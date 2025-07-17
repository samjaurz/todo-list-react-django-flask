import api from "@/lib/axios"


const getAllTask = async () => {
  try {
    const response = await api.get("/task"); 
    console.log("Get all entries", response.data);
    return response.data;
  } catch (error) {
    console.error("Error Axios", error);
  }
};



const searchTask = async (taskName: string) => {
       try {
        const response = await api.get(`task/${taskName}`)
        console.log('Search task', response)
        } catch( error) {
            console.error('Error filtering task', error);
        }

};



export { getAllTask , searchTask }
