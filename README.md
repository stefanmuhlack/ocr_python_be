# OCR Backend

## Endpoints

### Template Management

#### Create Template
```
POST /templates/

**Request Body:**
```json
{
  "name": "Test Template",
  "fields": [
    {"name": "Field1", "type": "text"},
    {"name": "Field2", "type": "boolean"}
  ]
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Template created successfully",
  "template_id": 1
}
```

#### Update Template
```
PUT /templates/{template_id}

**Request Body:**
```json
{
  "name": "Updated Template",
  "fields": [
    {"name": "UpdatedField1", "type": "text"}
  ]
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Template updated successfully"
}
```

#### Delete Template
```
DELETE /templates/{template_id}

**Response:**
```json
{
  "status": "success",
  "message": "Template deleted successfully"
}
```

## Running Tests

To run the tests, use the following command:
```
pytest
```
