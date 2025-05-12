from fastapi import APIRouter, Depends, HTTPException
from app.models.schemas import ChainConfiguration, ChainConfigurationResponse
from app.services.model_service import ModelService
from app.api.dependencies import get_model_service

router = APIRouter(tags=["chains"])


@router.post("/configure", response_model=ChainConfigurationResponse)
async def configure_chain(
    config: ChainConfiguration,
    model_service: ModelService = Depends(get_model_service)
):
    """
    Configure a customizable chain with a system message and parameters
    
    This gives the user the power to set a custom chain for instructions
    and parameters for the model.
    """
    try:
        chain_name = config.name or "customizable"

        if chain_name not in model_service.model_chains:
            raise HTTPException(status_code=404, detail=f"Chain '{chain_name}' not found")  
        
        chain = model_service.model_chains[chain_name]

        if not hasattr(chain, 'update_configuration'):
            raise HTTPException(status_code=400, detail=f"Chain '{chain_name}' is not configurable")
        
        # Update the chain configuration
        chain.update_configuration(
            system_message=config.system_message,
            parameters=config.parameters
        )

        # Return the current configuration
        return ChainConfigurationResponse(
            name=chain_name,
            system_message=config.system_message,
            parameters=config.parameters
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error configuring chain: {str(e)}")