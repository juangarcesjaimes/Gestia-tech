import { useEffect } from "react";
import { useForm } from "react-hook-form";
import { CreateClientes, deleteCliente, GetCliente, UpdateCliente } from "../api/ventas"; 
import { useNavigate, useParams } from "react-router-dom";
import toast from "react-hot-toast";


export function CrearCliente() {
    const { register, handleSubmit, formState: { errors }, setValue 
} = useForm();

    const navigate =useNavigate(); 
    const params = useParams();
    
    

    const onSubmit = async (data) => {
        try {
            if (params.id) {
                await UpdateCliente(params.id, data);
                console.log('Cliente actualizado con éxito');
            } else {
                await CreateClientes(data);
                console.log('Cliente creado con éxito');
                toast.success('Cliente creado con exito', {
                    position: "bottom-center",
                    style: {
                        background: "#202020",
                        color: "#fff"
                    }

                })
            }
        } catch (error) {
            console.error('Hubo un error al realizar la operación', error);
        }
        navigate("/lista-clientes");
    };
    
    useEffect(() => {
        async function loadCliente() {
            if (params.id) {
                console.log('obteniendo datos');
                const res = await GetCliente(params.id);
                setValue('nombre', res.data.nombre);
                setValue('apellido', res.data.apellido);
                setValue('email', res.data.email);
                setValue('telefono', res.data.telefono);
                setValue('direccion', res.data.direccion);
            }
        }
        loadCliente();
    }, [params.id, setValue]);
    
    return (
      <div className="max-w-xl mx-auto">
        <form onSubmit={handleSubmit(onSubmit)}>
            <input
                type="text"
                name="nombre"
                placeholder="Nombre"
                {...register("nombre", { required: true })}
                className="bg-zinc-700 p-3 rounded-lg block w-full mb-3"
            />
            {errors.nombre && <span>Este campo es obligatorio</span>}
            <input
                type="text"
                name="apellido"
                placeholder="Apellido"
                {...register("apellido", { required: true })}
                className="bg-zinc-700 p-3 rounded-lg block w-full mb-3"
            />
            {errors.apellido && <span>Este campo es obligatorio</span>}
            <input
                type="email"
                name="email"
                placeholder="Email"
                {...register("email", { required: true })}
                className="bg-zinc-700 p-3 rounded-lg block w-full mb-3"
            />
            {errors.email && <span>Este campo es obligatorio</span>}
            <input
                type="tel"
                name="telefono"
                placeholder="Teléfono"
                {...register("telefono", { required: true })}
                className="bg-zinc-700 p-3 rounded-lg block w-full mb-3"
            />
            {errors.telefono && <span>Este campo es obligatorio</span>}
            <textarea
                rows={2}
                name="direccion"
                placeholder="Dirección"
                {...register("direccion", { required: true })}
                className="bg-zinc-700 p-3 rounded-lg block w-full mb-3"
                
            />
            {errors.direccion && <span>Este campo es obligatorio</span>}
            <button className="bg-green-500 p-3 rounded-lg  w-48 mt-3">Guardar</button>
        </form>

        {params.id && (
        <button
          className="bg-red-500 p-3 rounded-lg w-48 mt-3"
          onClick={async () => {
            const aceptar =window.confirm("Estas seguro que quieres eliminar este cliente?");
            if (aceptar) {
                await deleteCliente(params.id);
                navigate("/lista-clientes");
            } 
          }}
        >Eliminar
        </button>
    )}

     </div>  
    );
}
