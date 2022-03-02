#version 330
#define M_PI 3.14159265358979

// #define N_WAVELENGTHS 10
// uniform vec3 iColor;
// uniform int nTextures;



// [pydefine]
// N_WAVELENTHS, EXPOSURE, etc here

// [/pydefine]



uniform sampler2DArray spectralTextures;

uniform vec2 mouse_pos;


uniform float _exposure;
// uniform float exposure;

uniform vec3[N_WAVELENGTHS] iCurve; // This will be replaced by the python shader.compile

in vec2 fTexcoords;

out vec4 out_color;


// [pyvars]
// [/pyvars]

//##########################################
//
//   Compiled
//
//##########################################

// [pyspace]
// [/pyspace]

//##########################################
//
//   Main code
//
//##########################################

// vec3 R = vec3(3.2404542, -1.5371385, -0.4985314);
// vec3 G = vec3(-0.9692660,  1.8760108,  0.0415560);
// vec3 B = vec3(0.0556434, -0.2040259,  1.0572252);
// // # Convert XYZ to RGB
// vec3 xyz2rgb(vec3 xyz) {
// 	// dot should be the same as np.sum(np.multiply(R, XYZ), axis = 1)?
// 	return vec3(dot(R, xyz),
// 							dot(G, xyz),
// 							dot(B, xyz));
// }

// Another conversion
// From: http://www.yaldex.com/open-gl/ch19lev1sec4.html
const mat3 CIEtoRGBmat = mat3(3.240479, -0.969256,  0.055648,
                             -1.537150,  1.875992, -0.204043,
                             -0.498535,  0.041556,  1.057311);
// vec3 rgbColor = cieColor * CIEtoRGBmat;
vec3 xyz2rgb(vec3 xyz) {
	return xyz * CIEtoRGBmat;
}


// From nori (gui.cpp)
// vec3 toSRGB(vec3 value) {
//     if (value < 0.0031308)
//         return 12.92 * value;
//     return 1.055 * pow(value, 0.41666) - 0.055;
// }
vec3 encodeSRGB(vec3 linearRGB)
{
    vec3 a = 12.92 * linearRGB;
    vec3 b = 1.055 * pow(linearRGB, vec3(1.0 / 2.4)) - 0.055;
    vec3 c = step(vec3(0.0031308), linearRGB);
    return mix(a, b, c);
}



void main()
{
		vec3 col3 = vec3(0.0);


		for(int i = 0; i < N_WAVELENGTHS; i++) // For each wavelength
		{ // add its contribution to each xyz channel given the curve
			col3 += iCurve[i] * texture(spectralTextures, vec3(fTexcoords,i)).r;
		}

    // float maxcoeff = max(max(col3.r, col3.g), col3.b);
    //if (maxcoeff>0.0 && maxcoeff<1.0) col3 /= maxcoeff;

    //col3 = xyz2rgb(col3);

    // col3 = vec3(toSRGB(col3.r),toSRGB(col3.r),toSRGB(col3.b));
    // col3 = encodeSRGB(col3);
    // col3 = xyz2rgb(col3);

    out_color = clamp(vec4(col3 * _exposure, 1.0), 0.0, 1.0);

    //
    // out_color=vec4(fTexcoords,0,1);
    // out_color = vec4(col3 * _exposure, 1.0);
    // out_color = vec4(0.7,0,0,1);

    // int i = int(_exposure);
    // vec3 col3 = iCurve[i];// * texture(spectralTextures, vec3(fTexcoords,i)).r;
    // out_color = vec4(col3, 1.0);


}



// -----------------------------------------------------------------------
// int i = int((1.0-mouse_pos.y) * nTextures);
// vec3 col3 = iCurve[i] * texture(spectralTextures, vec3(fTexcoords,i)).r;
// out_color = clamp(vec4(500.0*col3*mouse_pos.y, 1.0), 0.0, 1.0);
// -----------------------------------------------------------------------
// -----------------------------------------------------------------------
// out_color = clamp(vec4(0.5*iCurve[int(mouse_x)], 1.0), 0.0, 1.0);
// -----------------------------------------------------------------------
// int i = int(mouse_pos.x * nTextures);
// vec3 col3 = iCurve[i] * texture(spectralTextures, vec3(fTexcoords,i)).g;
// out_color = clamp(vec4(500.0*col3*mouse_pos.y, 1.0), 0.0, 1.0);
// -----------------------------------------------------------------------
// out_color = vec4(tex_idx,0.3,0.3,1.0);//texture(spectralTextures, vec3(fTexcoords,tex_idx));
