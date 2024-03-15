swagger: '2.0'
info:
  title: Langsearch Vertex AI Search API
  version: 1.0.0
paths:
  /:
    get:
      summary: Welcome message
      operationId: greet message
      responses:
        '200':
          description: Welcome message
          schema:
            type: object
            properties:
              status_code:
                type: integer
                example: 200
              message:
                type: string
                example: "WELCOME TO LANGSEARCH VERTEX AI SEARCH"
      security:
        - api_key: []
  /query:
    get:
      summary: Search products
      operationId:  search products
      parameters:
        - name: query
          in: query
          required: true
          type: string
      responses:
        '200':
          description: Search results
          schema:
            type: array
            items:
              type: object
              properties:
                id:
                  type: string
                product_name:
                  type: string
                category:
                  type: string
                price:
                  type: number
      security:
        - api_key: []
schemes:
  - https
x-google-backend:
   address: ${cloud_run_service_url}
securityDefinitions:
  api_key:
    type: apiKey
    name: key
    in: query