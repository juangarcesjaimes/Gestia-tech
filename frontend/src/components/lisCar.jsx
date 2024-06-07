import { useNavigate } from 'react-router-dom';
import PropTypes from 'prop-types';

export function Car ({cliente}) {

    const navigate = useNavigate();

    return(
        <div 
          className='bg-zinc-800 p-3 hover:bg-zinc-700 hover:cusor-pointer'

          onClick={() =>{
             navigate('/clientes/' + cliente.id) 
            }}
        >          
            <h1 className='fond-bold uppercase'>{cliente.nombre}</h1>
            <p className='text-slate-400'>{cliente.telefono}</p>
            
        </div>
    )
}

Car.propTypes = {
    cliente: PropTypes.shape({
        nombre: PropTypes.string.isRequired,
        telefono: PropTypes.string.isRequired,
    }).isRequired,
};

Car.propTypes = {
    cliente: PropTypes.shape({
        id: PropTypes.number.isRequired,
        nombre: PropTypes.string.isRequired,
        telefono: PropTypes.string.isRequired,
    }).isRequired,
};

