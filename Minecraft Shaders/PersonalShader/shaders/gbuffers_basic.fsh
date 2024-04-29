#version 120

varying vec2 TexCoords;
varying vec4 Color;
varying vec3 Normal;
varying vec2 LightmapCoords;

uniform sampler2D texture;
uniform sampler2D colortex4;

void main(){
	/* DRAWBUFFERS:0124 */
	gl_FragData[0] = vec4((texture2D(texture, TexCoords) * Color).rgba);
	gl_FragData[1] = vec4(Normal * 0.5f + 0.5f, 1.0f);
	gl_FragData[2] = vec4(LightmapCoords, 0.0f, 1.0f);
	gl_FragData[3] = vec4(vec3(0.1f),1.0f);
}