#version 120

varying vec2 TexCoords;
varying vec3 color;

void main() {
   gl_Position = ftransform();
   TexCoords = gl_MultiTexCoord0.st;
   color = gl_Color.rgb;
}