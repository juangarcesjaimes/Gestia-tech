import { Link } from "react-router-dom"

export function Navegacion() {
    return (
        <div className="flex justify-between py-5">
            <h1 className="font-bold text-3x1 mb-30">Ventas</h1>
            
             <button className="bg-blue-500 p-3 rounded-lg w-30 mt-3">
             <h3><Link to="/crear-cliente">Crear Cliente</Link></h3>
             </button>

             <button className="bg-blue-500 p-3 rounded-lg w-30 mt-3">
             <h3><Link to="/lista-clientes">Lista de clientes</Link></h3>
             </button> 
        </div>
    )
}