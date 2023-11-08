# En OpenGl, los shaders se escriben en lenguaje GLSL
# Graphics Library Shader Language

vertex_shader = '''
#version 450 core

layout (location = 0) in vec3 position;
layout (location = 1) in vec2 texCoords;
layout (location = 2) in vec3 normals;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;
uniform mat4 camMatrix;

out vec2 uvs;
out vec3 fragPosition;
out vec3 fragNormal;

void main()
{
	vec4 worldPosition = modelMatrix * vec4(position, 1.0);
	fragPosition = vec3(worldPosition);
	fragNormal = mat3(modelMatrix) * normals;

	gl_Position = projectionMatrix * viewMatrix * worldPosition;
	uvs = texCoords;
}

'''


fragment_shader = '''
#version 450 core

layout (binding = 0) uniform sampler2D tex;

in vec2 uvs;

out vec4 fragmentColor;

void main()
{
    fragmentColor = texture(tex, uvs);
}
'''


glow_shader = '''
#version 450 core

layout (binding = 0) uniform sampler2D tex;

in vec2 uvs;
in vec3 fragPosition;
in vec3 fragNormal;

uniform mat4 camMatrix;

out vec4 fragmentColor;

void main()
{
	vec4 textureColor = texture(tex, uvs);

	vec3 camForward = vec3(camMatrix[0][2], camMatrix[1][2], camMatrix[2][2]);
	vec3 normal = normalize(fragNormal);
	float glowAmount = 1.0 - dot(normal, normalize(camForward - fragPosition));
	if (glowAmount < 0) glowAmount = 0.0;

	vec3 glowColor = vec3(0, 1, 1);
	vec3 color = vec3(textureColor) + glowAmount * glowColor;
	color = clamp(color, 0.0, 1.0);

	fragmentColor = vec4(color, textureColor.a);
}
'''