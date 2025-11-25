{{- define "health-api.name" -}}
health-api
{{- end }}

{{- define "health-api.fullname" -}}
{{ include "health-api.name" . }}
{{- end }}