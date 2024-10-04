config = {
	"strategy": { "mode": "loadbalance" },
	"targets": [
		{
			"provider": "openai",
			"api_key": "xxx",
			"weight": 1,
			"override_params": { "model": "gpt-3.5-turbo" }
		},
		{
			"provider": "mistral-ai",
			"custom_host": "http://MODEL_URL/v1/",
			"weight": 1,
			"override_params": { "model": "mixtral-8x22b" }
		}
	]
}