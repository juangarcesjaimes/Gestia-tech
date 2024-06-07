import axios from "axios";


const ventasApi =axios.create({
    baseURL: "http://localhost:8000/cliente/api/v1/cliente/"
});

export const getAllVentas = () => ventasApi.get("/")
export const GetCliente = (id) => ventasApi.get(`/${id}/`);
export const CreateClientes = (Cliente) => ventasApi.post("/", Cliente)
export const deleteCliente =(id) => ventasApi.delete(`/${id}/`)
export const UpdateCliente =(id, Cliente) => ventasApi.put(`/${id}/`, Cliente)