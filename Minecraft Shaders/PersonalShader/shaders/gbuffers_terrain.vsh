#version 120

attribute vec4 mc_Entity;

varying vec2 TexCoords;
varying vec3 Normal;
varying vec2 LightmapCoords;
varying float isFoliage;

varying vec4 Color;

void main() {
	gl_Position = ftransform();
	TexCoords = gl_MultiTexCoord0.st;
	Normal = gl_NormalMatrix * gl_Normal;
	Color = gl_Color;
	if(mc_Entity.x == 10000.0){isFoliage = 1.0f;}
	else{isFoliage=0.0f;}
	// Use the texture matrix instead of dividing by 15 to maintain compatiblity for each version of Minecraft
    LightmapCoords = mat2(gl_TextureMatrix[1]) * gl_MultiTexCoord1.st;
    // Transform them into the [0, 1] range
    LightmapCoords = (LightmapCoords * 33.05f / 32.0f) - (1.05f / 32.0f);
}