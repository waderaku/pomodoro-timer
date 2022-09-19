import dayjs from "dayjs";
import { ChangeEvent, useState } from "react";
import { atom, useRecoilState } from "recoil";
import {
  Deadline,
  Minute,
  Notes,
  ShortcutFlg, TaskConfigModel, TaskConfigViewModel,
  TaskId, TaskName
} from "../model";

const taskConfigState = atom<TaskConfigModel>({
  key: "taskConfig",
  default: null,
});

const useTaskConfigViewModel = (): TaskConfigViewModel => {
  const [taskConfig, setTaskConfig] = useRecoilState(taskConfigState);
  const isModalOpen = taskConfig ? true : false;
  const [updateTaskProps, setupdateTaskProps] = useState({
    name: "",
    estimatedWorkload: 0,
    deadline: dayjs(),
    notes: "",
    shortcutFlg: false,
  });
  const handleConfigOpen = (taskId: TaskId) => {
    setTaskConfig(taskId);
  };
  const handleConfigClose = () => {
    setTaskConfig(null);
  };
  const handleUpdate = (
    updateTask: (
      taskName: TaskName,
      estimatedWorkload: Minute,
      deadline: Deadline,
      notes: Notes,
      shortcutFlg: ShortcutFlg
    ) => void
  ) => {
    updateTask(
      updateTaskProps.name,
      updateTaskProps.estimatedWorkload,
      updateTaskProps.deadline,
      updateTaskProps.notes,
      updateTaskProps.shortcutFlg
    );
    handleConfigClose();
  };
  const handleUpdateName = (
    e: ChangeEvent<HTMLTextAreaElement | HTMLInputElement>
  ) => {
    setupdateTaskProps({
      ...updateTaskProps,
      name: e.target.value,
    });
  };
  const handleUpdateEstimatedWorkload = (
    e: ChangeEvent<HTMLTextAreaElement | HTMLInputElement>
  ) => {
    setupdateTaskProps({
      ...updateTaskProps,
      estimatedWorkload: Number(e.target.value),
    });
  };
  const handleUpdateDeadline = (e: Deadline) => {
    if (e) {
      setupdateTaskProps({
        ...updateTaskProps,
        deadline: e,
      });
    }
  };
  const handleUpdateShortcutFlg = (e: ChangeEvent<HTMLInputElement>) => {
    setupdateTaskProps({
      ...updateTaskProps,
      shortcutFlg: e.target.checked,
    });
  };
  const handleUpdateNotes = (
    e: ChangeEvent<HTMLTextAreaElement | HTMLInputElement>
  ) => {
    setupdateTaskProps({
      ...updateTaskProps,
      notes: e.target.value,
    });
  };
  return {
    taskConfig,
    isModalOpen,
    updateTaskProps,
    setupdateTaskProps,
    handleConfigOpen,
    handleConfigClose,
    handleUpdate,
    handleUpdateName,
    handleUpdateEstimatedWorkload,
    handleUpdateDeadline,
    handleUpdateShortcutFlg,
    handleUpdateNotes,
  };
};

export default useTaskConfigViewModel