import { useEffect, useState } from "react";
import {Car,} from "./lisCar"
import { getAllVentas } from "../api/ventas";


export function ClienteLis() {
    const [clientes, setClientes] = useState([]);

    useEffect(() => {
        async function cargarClientes() {
            try {
                const res = await getAllVentas();
                setClientes(res.data);
            } catch (error) {
                console.error("Error al cargar los datos:", error);
            }
        }
        cargarClientes();
    }, []);

    return (
        <div className="grid grid-cols-3 gap-3">
            {clientes.map((cliente) => (
            
                <Car key= {cliente.id} cliente={cliente} />
            ))}
        </div>
    );
}
