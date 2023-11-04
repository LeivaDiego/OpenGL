# En OpenGl, los shaders se escriben en lenguaje GLSL
# Graphics Library Shader Language

vertex_shader = '''
#version 450 core

layout (location = 0) in vec3 position;
layout (location = 1) in vec2 texCoords;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

uniform float time;

out vec2 uvs;

void main()
{
	vec4 newPos = vec4(position.x, position.y + sin(time)/4, position.z, 1.0);

	gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(newPos);
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

starman_vertex = '''
#version 450 core

layout (location = 0) in vec3 position;
layout (location = 1) in vec2 texCoords;
layout (location = 2) in vec3 normal;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;
uniform mat4 normalMatrix;
uniform vec3 camPosition;

out vec2 fragmentTexCoords;
out vec3 fragmentNormal;
out vec3 toCameraVector;

void main() {
	vec4 worldPosition = modelMatrix * vec4(position, 1.0);
	gl_Position = projectionMatrix * viewMatrix * worldPosition;
	fragmentTexCoords = texCoords;
	fragmentNormal = (normalMatrix * vec4(normal, 0.0)).xyz;
	toCameraVector = camPosition - worldPosition.xyz;
}

'''

starman_fragment = '''
#version 450 core

layout (binding = 0) uniform sampler2D tex;

in vec2 fragmentTexCoords;
in vec3 fragmentNormal;
in vec3 toCameraVector;

out vec4 fragmentColor;

const float pi = 3.14159265359;

void main() {
	vec3 normalizedNormal = normalize(fragmentNormal);
	vec3 normalizedToCameraVector = normalize(toCameraVector);

	float glowAmount = 1.4 - dot(normalizedNormal, normalizedToCameraVector);
	glowAmount = max(glowAmount, 0.0);

	float diagonalValue = (fragmentTexCoords.x + fragmentTexCoords.y) * 0.5;
	vec3 rainbowGlow = vec3(abs(sin(diagonalValue * 2.0 * pi)),
							abs(sin((diagonalValue + 1.0 / 3.0) * 2.0 * pi)),
							abs(sin((diagonalValue + 2.0 / 3.0) * 2.0 * pi)));

	vec3 textureColor = texture(tex, fragmentTexCoords).rgb;
	vec3 finalColor = textureColor + glowAmount * rainbowGlow;
	fragmentColor = vec4(finalColor, 1.0);
}

'''