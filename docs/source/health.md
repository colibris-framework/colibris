# Health Status

You can (and should) implement your project-specific health check function by exposing the `get_health` function in
`app.py`:

    def get_health():
        if not persist.connectivity_check():
            raise app.HealthException('database connectivity check failed')
    
        return 'healthy'
