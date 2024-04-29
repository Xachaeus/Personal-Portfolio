#version 120

varying vec2 TexCoords;
varying vec3 Normal;
varying vec2 LightmapCoords;
varying float isFoliage;

varying vec4 Color;

uniform sampler2D texture;
uniform sampler2D lightmap;
uniform sampler2D depthtex0;
uniform sampler2D colortex4;

void main() {
	vec4 albedo = texture2D(texture, TexCoords) * Color;
	/* DRAWBUFFERS:0124 */
	gl_FragData[0] = albedo;
	gl_FragData[1] = vec4(Normal * 0.5f + 0.5f, 1.0f);
	gl_FragData[2] = vec4(LightmapCoords, 0.0f, 1.0f);
	float GrassMaskData = texture2D(colortex4, TexCoords).r;
	gl_FragData[3] = vec4( GrassMaskData != 0.1f? isFoliage : 0.1f,0.0f,0.0f,1.0f);
	//gl_FragData[3] = vec4(vec3(0.1f),1.0f);
}