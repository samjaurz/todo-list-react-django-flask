"use client";
import api from "@/lib/axios"
import SearchBar from "@/components/SearhBar";
import Table from "@/components/Table"
import { useEffect, useState } from "react";
import { getAllTask } from "@/services/taskService";

interface Task {
    id: number;
    name: string;
    status: boolean;
    editable?: boolean;
};

export default function Home() {
  const [tasks, setTasks] = useState([]);
  const [editingId, setEditingId] = useState<number | null>(null);
  const [updateTask, setUpdateTask] = useState({id:"", name:"", status:""});


  useEffect(() => {
    getAllTask().then((data) => {
      setTasks(data ?? []);
    });
  }, []);

  const updateTasks = (updatedTasks)=> {
    setTasks(updatedTasks)
  }

  const handleEdit = (task: Task) => 
    setEditingId(task.id)
    console.log(editingId);

  // const handleSave = (updated: Task) => {
  //   setUpdateTask(updated)
  //   setTasks((prev) =>
  //     prev.map((t) => (t.id === updated.id ? updated : t))
  //   );
  //   console.log("sss",updateTask)
  //   setEditingId(null);
  // };

  
  const handleSave = async (updated: Task) => {
      setTasks((prev) =>
      prev.map((t) => (t.id === updated.id ? updated : t))
    );
      const payload = {
        name: updated.name,
        status: updated.status
      };
      const response = await api.put(`task/${updated.id}`, payload);
      console.log(response);
      setEditingId(null);
    }

    
  return (
    <div className="pl-10 pr-10">
      <div className="justify-center items-center flex text-5xl py-10 font-bold">
        <h1>TODO LIST</h1>
      </div>
      <div>
        <SearchBar
          tasks={tasks} 
          updateTasks={updateTasks}
          onEdit={handleEdit}
        />
        <main>
        <Table
          tasks={tasks}
          updateTasks={updateTasks}
          editingId={editingId}
          onEdit={handleEdit}
          onSave={handleSave}
          setEditingId={setEditingId}
        />
        </main>
      </div>
    </div>
  );
}
