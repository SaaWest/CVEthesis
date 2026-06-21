def pocPrompt(context: dict) -> str:
    return [
        {
            "role": "system",
            "content":"You are to create working PoC files needed for the CVE. Provided are the CVE identifier, package with version, url containing exploit, and the text from the website."
        },
        {
            "role": "user",
            "content": f"""
        CVE:
        {context['cveID']}

        Package:
        {context['pkg']}

        Version:
        {context['version']}

        References:
        {context['ref']}

        PoC:
        {context['ref_text']}

        Return JSON:
        {{
        "files":[{{"path": "", "content": ""}}],
        "run_commands": [],
        "expected_behavior": "",
        "success_indicators": []
        }}
        """

        }
    ]