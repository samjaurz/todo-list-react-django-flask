"use client";

import SearchBar from "@/components/SearhBar";
import Table from "@/components/Table";
import {useEffect, useState} from "react";
import getApiInstance from "@/lib/axios";
import Dropdown from "@/components/Dropdown";

interface Task {
    id: number;
    name: string;
    status: boolean;
}

interface User {
    id: number,
    name: string,
    last_name: string,
    status: boolean
}

export default function Home() {
    const [tasks, setTasks] = useState<Task[]>([]);
    const [editingId, setEditingId] = useState<number | null>(null);
    const [apiSelection, setApiSelection] = useState(false)
    const [users, setUsers] = useState<User[]>([]);

    const api = getApiInstance(apiSelection);

    const getAllTask = async () => {
        try {
            const response = await api.get("/tasks/");
            console.log("Get all entries", response.data);
            return response.data;
        } catch (error) {
            console.error("Error Axios", error);
        }
    };

    const getAllUser = async () => {
        try {
            const response = await api.get("/users/");
            console.log("Get all users", response.data);
            return response.data;
        } catch (error) {
            console.error("Error Axios", error);
        }
    };


    useEffect(() => {
        getAllTask().then((data) => {
            setTasks(data ?? []);
        });
    }, [apiSelection]);

    useEffect(() => {
        getAllUser().then((data) => {
            setUsers(data ?? []);
        });
    }, []);

    console.log("users", users)
    const handleEdit = (task: Task) => {
        console.log("task edit", task.id)
        const alreadyExist = tasks.some(task => task.id === 0);
        if (alreadyExist) {
            if (task.id !== 0) {
                tasks.shift()
                setEditingId(null)
            }
        }
        setEditingId(task.id)
    }
    const handleCancel = (task: Task) => {
        if (task.id === 0) {
            const newTasks = tasks.filter(t => t.id !== 0);
            setTasks(newTasks);
        }
        setEditingId(null)

    }
    const handlerAdd = () => {

        const addId_0 = tasks.some(task => task.id === 0);
        if (addId_0) {
            return
        }

        const new_tasks = [{
            id: 0,
            status: false,
            name: ""
        }, ...tasks];

        console.log("new_task added", new_tasks)
        setTasks(new_tasks)
        handleEdit(new_tasks[0])
    }
    const handleSearch = async (searchTask: string) => {
        console.log("search handle", searchTask)
        const response = await api.get(`tasks/search?name=${searchTask}`)
        console.log("response handle search after api", response)
        setTasks(response.data)
    }
    const handleSave = async (updated: Task) => {
        console.log("updated", typeof (updated.status))
        if (updated) {
            const payload = {
                name: updated.name,
                status: updated.status
            }
            if (editingId === 0) {
                const response = await api.post('tasks/', payload);
                console.log("post response", response);
                setTasks((prev) => {
                    prev = [...prev];
                    response.data.status = payload.status
                    prev.shift();
                    return [...prev, response.data];
                });
            } else {
                const response = await api.put(`tasks/${updated.id}`, payload);
                console.log("update response", response);
                setTasks((prev) =>
                    prev.map((t) => (t.id === updated.id ? updated : t))
                );
            }
            setEditingId(null);
        }
    }
    const handleDelete = async (task: Task) => {
        console.log("Deleting task", task.id)
        const response = await api.delete(`/tasks/${task.id}`);
        console.log("delete", response)
        const filteredTasks = tasks.filter(el => el.id != task.id);
        setTasks(filteredTasks)
    }

    const handleFilterUser = async  (user:User) =>{
        console.log(user,"www")
        const response = await api.get(`users/${user}/tasks`)
        setTasks(response.data);
    }

    return (
        <div className="pl-10 pr-10">
            <div className="justify-center items-center flex text-5xl py-10 font-bold">
                <h1>TODO LIST</h1>
            </div>
            <div className="justify-end flex p-3">
                 <Dropdown
                     users={users}
                    handleFilterUser = {handleFilterUser}
                 />
            </div>

            <SearchBar
                tasks={tasks}
                handleSearch={handleSearch}
                handlerAdd={handlerAdd}
                setApiSelection={setApiSelection}
            />
            <div className={`text-center items-end ${apiSelection ? "bg-green-400" : "bg-amber-200"}`}>
                <h1>{apiSelection ? "Django API" : "Flask API"}</h1>
            </div>
            <main>
                <Table
                    tasks={tasks}
                    editingId={editingId}
                    onEdit={handleEdit}
                    onSave={handleSave}
                    setEditingId={setEditingId}
                    onDelete={handleDelete}
                    handleCancel={handleCancel}
                />
            </main>
        </div>
    );
}
