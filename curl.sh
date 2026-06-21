curl -sSf https://api.osv.dev/v1/query \
  -d '{
    "version": "2.0.0",
    "package": {
      "name": "pydicom",
      "ecosystem": ""
    }
  }' | jq
