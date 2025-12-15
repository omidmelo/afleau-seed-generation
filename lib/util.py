from .secret_handler import SecretHandler

def get_pg_conn_string(in_vpc=False, env='dev'):
    """
    Get PostgreSQL connection string.
    
    Args:
        in_vpc: Whether to use VPC private IP (default: False)
        env: Environment - 'dev' or 'prod' (default: 'dev')
              Note: Currently both environments use the same 'afleau' database.
              This parameter is kept for future use and consistency.
    
    Returns:
        PostgreSQL connection string
    """
    afleau_user = SecretHandler.get_secret_value("AFLEAU_PG_USER")
    afleau_pass = SecretHandler.get_secret_value("AFLEAU_PG_PASS")
    ip_key = "AFLEAU_PG_IP_PRIVATE" if in_vpc else "AFLEAU_PG_IP"
    afleau_ip = SecretHandler.get_secret_value(ip_key)
    
    # Validate env parameter
    if env not in ['dev', 'prod']:
        raise ValueError(f"Invalid env parameter: {env}. Must be 'dev' or 'prod'")
    
    # Database name - currently the same for both environments
    db_name = "afleau"
    
    return f"postgresql://{afleau_user}:{afleau_pass}@{afleau_ip}:5432/{db_name}?options=-csearch_path%3Dafleau"