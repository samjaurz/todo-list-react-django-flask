"use client";
import api from "@/lib/axios"
import SearchBar from "@/components/SearhBar";
import Table from "@/components/Table"
import {useEffect, useState} from "react";
import {getAllTask} from "@/services/taskService";

interface Task {
    id: number;
    name: string;
    status: boolean;
}

export default function Home() {
    const [tasks, setTasks] = useState<Task[]>([]);
    const [editingId, setEditingId] = useState<number | null>(null);

    useEffect(() => {
        getAllTask().then((data) => {
            setTasks(data ?? []);
        });
    }, []);


    const handleEdit = (task: Task) => setEditingId(task.id)

    const handlerAdd = (addNewRow: any) => {
        setTasks(addNewRow)
    }
    const handleSearch = async (searchTask: string) => {
        console.log("search handle", searchTask)
        const response = await api.get(`task/search?name=${searchTask}`)
        console.log("response handle search after api", response)
        setTasks(response.data)
    }

    //     const filtered = tasks.filter((task) => {
    //         return task.name.toLowerCase().includes(addNewRow.toLowerCase());
    //     })
    //     setTasks(filtered)
    // }

    const handleSave = async (updated: Task) => {
        console.log("updated", typeof (updated.status))
        if (updated) {
            const payload = {
                name: updated.name,
                status: updated.status
            }
            if (editingId === 0) {
                const response = await api.post('task', payload);
                console.log("post response", response);
                setTasks((prev) => {
                    prev = [...prev];
                    response.data.status = payload.status
                    prev.shift();
                    return [...prev, response.data];
                });
            } else {
                const response = await api.put(`task/${updated.id}`, payload);
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
        const response = await api.delete(`/task/${task.id}`);
        console.log("delete",response)
        const filteredTasks = tasks.filter(el => el.id != task.id);
        setTasks(filteredTasks)
    }

    return (
        <div className="pl-10 pr-10">
            <div className="justify-center items-center flex text-5xl py-10 font-bold">
                <h1>TODO LIST</h1>
            </div>
            <div>
                <SearchBar
                    tasks={tasks}
                    onEdit={handleEdit}
                    handleSearch={handleSearch}
                    handlerAdd = {handlerAdd}
                />
                <main>
                    <Table
                        tasks={tasks}
                        editingId={editingId}
                        onEdit={handleEdit}
                        onSave={handleSave}
                        setEditingId={setEditingId}
                        onDelete={handleDelete}
                        handlerAdd={handlerAdd}
                    />
                </main>
            </div>
        </div>
    );
}
