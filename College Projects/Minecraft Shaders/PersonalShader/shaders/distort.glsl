#ifndef DISTORT_GLSL
#define DISTORT_GLSL


vec2 DistortPosition(in vec2 position){

    float CenterDistance = length(position);
    float DistortionFactor = mix(1.0f, CenterDistance, 0.9f);
    return position / DistortionFactor;

	float distort_factor = 0.1f;
	float factor = length(position) + distort_factor;
	return position / factor;

}

float computeBias(in vec2 pos){
	float numerator = length(pos) + 0.1f;
	numerator *= numerator;
	return 0.05f / 4096.0f * numerator / 0.1f;
}

#endif