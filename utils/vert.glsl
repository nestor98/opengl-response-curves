#version 330

out vec2 fTexcoords;

void main()
{
    vec2 pos = vec2(gl_VertexID % 2, gl_VertexID / 2) * 4.0 - 1.0;
    fTexcoords = pos * 0.5 + 0.5;
		fTexcoords.y = 1.0-fTexcoords.y;
    gl_Position = vec4(pos, 0.0, 1.0);
}
