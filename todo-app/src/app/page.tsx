"use client";
import BarTask from "@/components/bar_task";
import SearchBar from "@/components/search_bar";
import { useEffect, useState } from "react";
import { getAllTask } from "@/services/taskService";

export default function Home() {
  const [tasks, setTasks] = useState(null);
  const [selectedTask, setSelectedTask] = useState("");


  useEffect(() => {
    getAllTask().then((data) => {
      console.log("data", data)
      if (data == undefined)
        data = []
      setTasks(data);
      console.log("renderizado de tabla setTask" , setTasks(data))
    });
  }, []);
  if (!tasks) return null;

  const updateTasks = (updatedTasks)=> {
    setTasks(updatedTasks)
  }

  const onSelectTask = (task) =>{
    task.editable = true
    console.log("selected task hook", task)
    setSelectedTask(task)
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
          onSelectTask={onSelectTask}
        />
        <BarTask
          tasks={tasks} 
          updateTasks={updateTasks}
        />
      </div>
    </div>
  );
}
