#version 120
#include "distort.glsl"

varying vec2 TexCoords;
varying vec3 color;
varying float isFoliage;

uniform vec3 shadowLightPosition;
uniform vec3 sunPosition;
uniform float sunAngle;
uniform vec3 skyColor;
uniform int worldTime;
uniform vec3 cameraPosition;

uniform sampler2D colortex0;
uniform sampler2D colortex1;
uniform sampler2D colortex2;
uniform sampler2D colortex3;
uniform sampler2D colortex4;

uniform sampler2D depthtex0;
uniform sampler2D shadowtex0;
uniform sampler2D shadowtex1;
uniform sampler2D shadowcolor0;

uniform sampler2D noisetex;
uniform sampler2D lightmap;

uniform mat4 gbufferProjectionInverse;
uniform mat4 gbufferModelViewInverse;
uniform mat4 shadowModelView;
uniform mat4 shadowProjection;

/*
const int colortex0Format = RGBA16;
const int colortex1Format = RGBA16;
const int colortex2Format = RGB16;
const int colortex3Format = RGB16;
const int colortex4Format = RGBA16;

*/

#define SHADOW_BLUR 1.0 // Shadow Blur [0.0 0.25 0.5 0.75 1.0 1.5 2.0]
#define AO_STRENGTH 1.5 // Ambient Occlusion Strength [0.0 0.5 1.0 1.5 2.0 2.2 2.5 2.75 3.0 3.25 3.5]

const float sunPathRotation = -40.0;
const int shadowMapResolution = 4096;
const bool shadowcolor0Nearest = true;
const bool shadowtex0Nearest = true;
const bool shadowtex1Nearest = true;
const float ambient = 0.005f;
const float sun_luminence = 2.7f;//1.8f;
const float sky_luminence = 1.4f;
const float night_sky_luminence = 0.10f;
const float torch_luminence = 1.5f; 
const float moon_luminence = 0.3f;
const float shadow_blur = SHADOW_BLUR;
const float sunrise_duration = 0.9f;
const float day_begin = 23300.0f;
const float day_end = 12700.0f;
const float night_start = 13000.0f;
const float night_end = 23000.0f;
const float AO_strength = AO_STRENGTH;
const float shadow_bias = 1.0f;
const float directional_illumination_bias = 0.25f;
const float caveLightLeakFixLevel = 50.0f;
const float night_lightmap_weight = 0.3f;


float luminence(in vec3 color){
	return (0.2126f * color.r + 0.7152f * color.g + 0.0722f * color.b);

}


float AdjustLightmapTorch(in float torch) {
    const float K = 2.0f;
    const float P = 5.06f;
    return K * pow(torch, P);
}

float AdjustLightmapSky(in float sky){
    float sky_2 = sky * sky;
    return sky_2 * sky_2;
}

vec2 AdjustLightmap(in vec2 Lightmap){
    vec2 NewLightMap;
    NewLightMap.x = AdjustLightmapTorch(Lightmap.x);
    NewLightMap.y = AdjustLightmapSky(Lightmap.y);
    return NewLightMap;
}

vec3 shadow_coords(vec3 position){
	vec3 ClipSpace = position * 2.0f - 1.0f;
    vec4 ViewW = gbufferProjectionInverse * vec4(ClipSpace, 1.0f);
    vec3 View = ViewW.xyz / ViewW.w;
    vec4 World = gbufferModelViewInverse * vec4(View, 1.0f);
    vec4 ShadowSpace = shadowProjection * shadowModelView * World;
    ShadowSpace.xy = DistortPosition(ShadowSpace.xy);
	ShadowSpace.z = ShadowSpace.z * 0.2f;
    return ShadowSpace.xyz * 0.5f + 0.5f;
}

float Visibility(in sampler2D ShadowMap, vec3 SampleCoords) {

	//vec4 normal = vec4(normalize(texture2D(colortex1, TexCoords).rgb * 2.0f - 1.0f), 1.0f);
	//normal = shadowProjection * shadowModelView * gbufferModelViewInverse * normal;
	float bias = computeBias(SampleCoords.xy);
	
	
	//float bias = 0.0001f;
	float shadow_depth = texture2D(ShadowMap, SampleCoords.xy).r;
	float actual_depth = SampleCoords.z-bias;
	return shadow_depth < actual_depth ? 0.0f : 1.0f;
	
	
	//return clamp((texture2D(ShadowMap, SampleCoords.xy).r-(SampleCoords.z-bias))*65536.0f,0.0,1.0);
}

vec3 TransparentShadow(in vec3 SampleCoords){
    float ShadowVisibility0 = Visibility(shadowtex0, SampleCoords);
	//return vec3(ShadowVisibility0);
    float ShadowVisibility1 = Visibility(shadowtex1, SampleCoords);
    vec4 ShadowColor0 = texture2D(shadowcolor0, SampleCoords.xy);
    vec3 TransmittedColor = ShadowColor0.rgb * (1.0f - ShadowColor0.a); // Perform a blend operation with the sun color
    return mix(TransmittedColor * ShadowVisibility1, vec3(1.0f), ShadowVisibility0);
}

#define SHADOW_SAMPLES 2
const int ShadowSamplesPerSize = 2 * SHADOW_SAMPLES + 1;
const float shadowDistance = 256.0f;
const float shadowIntervalSize = 2.0f;
const int TotalSamples = ShadowSamplesPerSize * ShadowSamplesPerSize;
const int noiseTextureResolution = 128;


vec3 GetShadow(float depth) {

	//if(cameraPosition.y<=caveLightLeakFixLevel){return vec3(0.0f);}
	
	//Get coordinates in shadow space
	vec3 SampleCoords = shadow_coords(vec3(TexCoords, depth));
	/*
	SampleCoords = vec3(0.0f);
	return vec3(Visibility(shadowtex0, SampleCoords));
	*/
	
	
    float RandomAngle = texture2D(noisetex, TexCoords * 20.0f).r * 100.0f;
    float cosTheta = cos(RandomAngle);
	float sinTheta = sin(RandomAngle);
    mat2 Rotation =  mat2(cosTheta, -sinTheta, sinTheta, cosTheta) / shadowMapResolution; // We can move our division by the shadow map resolution here for a small speedup
    vec3 ShadowAccum = vec3(0.0f);
    for(int x = -SHADOW_SAMPLES; x <= SHADOW_SAMPLES; x++){
        for(int y = -SHADOW_SAMPLES; y <= SHADOW_SAMPLES; y++){
            vec2 Offset = Rotation * vec2(x, y);
            vec3 CurrentSampleCoordinate = vec3(SampleCoords.xy + Offset*shadow_blur, SampleCoords.z);
            ShadowAccum += TransparentShadow(CurrentSampleCoordinate);
        }
    }
    ShadowAccum /= TotalSamples;
    return ShadowAccum;
	
}

/*Work in progress:*/
vec3 GetVolumetricLighting(vec3 color, float depth){
	float sum=0.0f;
	for(float d = 0.002f; d < depth; d += depth/200.0f){
		vec3 coords = shadow_coords(vec3(TexCoords, d));
		sum += max(sign(texture2D(shadowtex0, coords.xy).r - coords.z), 0.0f)*exp(-d*2.0);
	}
	return color * (sum/200.0f);
	
}

void main() {
	/* DRAWBUFFERS:0 */
	vec3 Albedo = pow(texture2D(colortex0, TexCoords).rgb, vec3(2.2f));
	float base_AO = texture2D(colortex0, TexCoords).a;
	float AOval = pow(base_AO, AO_STRENGTH);
	float direct_light_AOval = pow(base_AO, 3.0f);
	float Depth = texture2D(depthtex0, TexCoords).r;
	vec3 TerrainInfo = texture2D(colortex4, TexCoords).rgb;
	if(Depth == 1.0f){
		gl_FragData[0] = vec4(Albedo, 1.0f);
		gl_FragData[1] = vec4(vec3(luminence(Albedo)), 1.0f);
		return;
	}
	vec2 Lightmap = texture2D(colortex2, TexCoords).rg;
	Lightmap = AdjustLightmap(Lightmap);
	vec3 Normal = normalize(texture2D(colortex1, TexCoords).rgb * 2.0f - 1.0f);
	float NdotL = dot(Normal, normalize(shadowLightPosition));
	
	float facing_light = NdotL >= -0.25f ? 1.0f : 0.0f;
	//float facing_light = shadowLightPosition.z>=0.0f ? 1.0f : 0.0f;
	
	NdotL = max(directional_illumination_bias * NdotL + sign(NdotL)*(1.0f-directional_illumination_bias), 0.0f);
	
	float sun_val = abs(0.5f - 2*mod(sunAngle, 0.5))*2;
	float horizon_val = pow(sun_val, sunrise_duration);
	vec3 sunColor = vec3(1.0f, 0.85f-(horizon_val*0.5f),0.6f-(horizon_val*0.6f));
	vec3 moonColor = vec3(0.2f, 0.4f, 1.0f);
	vec3 torchColor = vec3(1.0f, 0.5f, 0.2f);
	
	float day_offset = (24000.0f-day_begin);
	float day_middle = (day_end + day_offset)/2.0f;
	float day_time = (worldTime+day_offset) >= day_middle+12000.0f ? (worldTime+day_offset)-24000.0f : (worldTime+day_offset);
	float sun_brightness = min(  pow((day_middle - min(abs(day_time-day_middle), day_middle))/day_middle, 0.6f),   0.6f);
	
	float night_middle = mod(night_end + (24000.0f - night_start), 24000.0f)/2.0f;
	float moon_brightness = max(pow((night_middle - min(abs(mod(worldTime+(24000.0f - night_start), 24000.0f)-night_middle), night_middle))/night_middle, 0.6f), 0.0f);
	
	vec3 shadow = GetShadow(Depth);
	
	//vec3 volumetricLight = GetVolumetricLighting(sunColor, Depth);
	
	vec3 sunLight = direct_light_AOval*sunColor*shadow*(TerrainInfo.r==1.0f ? (facing_light==0.0f ? vec3(0.4,1.0f,0.1f) : vec3(1.0f)) : vec3(NdotL))*sun_luminence*sun_brightness;
	
	vec3 moonLight = AOval*moonColor*shadow*NdotL*moon_luminence*moon_brightness;
	//pow(1.0f - abs(0.5f - 2*mod(sunAngle, 0.5))*2, 0.7f)*
	vec3 daySkyLight = AOval*skyColor*Lightmap.y*sky_luminence*sun_brightness;
	vec3 nightSkyLight = AOval*moonColor*(Lightmap.y*night_lightmap_weight + 1.0f-night_lightmap_weight)*night_sky_luminence*moon_brightness;
	vec3 torchLight = AOval*torchColor*Lightmap.x*torch_luminence;
	vec3 ambientLight = vec3(1.0f)*pow(AOval,0.8f)*ambient;
	
	
	vec3 Diffuse = Albedo * (sunLight + moonLight + daySkyLight + nightSkyLight + torchLight + ambientLight);//  + volumetricLight;
	gl_FragData[0] = vec4(Diffuse, 1.0f);
	//gl_FragData[0] = vec4(GetShadow(Depth), 1.0f);
	//gl_FragData[0] = vec4(Normal, 1.0f);
	//gl_FragData[0] = texture2D(shadowcolor0, TexCoords);
	//gl_FragData[0] = texture2D(colortex2, TexCoords);
	//gl_FragData[0] = vec4(texture2D(colortex4, TexCoords).rrr, 1.0f);
	//gl_FragData[0] = vec4(Depth-texture2D(depthtex0, TexCoords).r, TerrainInfo.g-Depth, TerrainInfo.r, 1.0f);
	//gl_FragData[0] = vec4(vec3(TerrainInfo.g-texture2D(depthtex0, TexCoords).r), 1.0);
	
}