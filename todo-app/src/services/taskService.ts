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

const addTask = async (taskName: string, statusTask: boolean) => {
    try {
        const payload = {
            name: taskName,
            status: statusTask,
        };
    const response = await api.post('task', payload);
    const newTask = response.data;
    console.log('Task created:', newTask);
    } catch (error) {
    console.error('Error adding task:', error);
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
   
const updateTask = async (taskId: number, taskName: string, statusTask: boolean) => {
    try {
        const payload = {
        name: taskName,
        status: statusTask,
    };
    const response = await api.put(`task/${taskId}`, payload);
    console.log('Task updated', response.data);
    return response.data
    }catch (error) {
    console.error('Error updating task', error);
    }
};


const deleteTask = async (taskId: number, setTask) => {
    try {
        const response = await api.delete(`/task/${taskId}`);
        console.log("Response status:", response.status); 
        console.log("Deleted task", taskId);
        setTask()
    }  
    catch (error) {
        console.log('Error deleting task:', error)
    }
}   

export { getAllTask , addTask , updateTask, deleteTask, searchTask }
