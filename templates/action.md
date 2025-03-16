# {{ action.name }} Action

{{ action.description }}

**Method:** {{ action.method }}  
**Endpoint:** {{ action.endpoint }}

## Parameters

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |

{% for param in action.parameters %}
| {{ param.name }} | {{ param.type }} | {{ param.description }} | {{ param.required }} |
{% endfor %}

## Example Request

```json
{{ action.example }}
```

## Usage

To use this action, send a POST request to the endpoint with a JSON body containing the required parameters.
