import { TaskDeleteModel, TaskDeleteViewModel, TaskId } from "domain/model";
import { atom, useRecoilState } from "recoil";

const taskDeleteState = atom<TaskDeleteModel>({
  key: "taskDelete",
  default: "",
});


const useTaskDeleteViewModel = (): TaskDeleteViewModel => {
  const [deleteTaskId, setDeleteTaskId] = useRecoilState(taskDeleteState);
  const handleDeleteScreenOpen = (taskId: TaskId) => {
    setDeleteTaskId(taskId);
  };
  const handleDeleteScreenClose = () => {
    setDeleteTaskId("");
  };
  const isDeleteModalOpen = deleteTaskId ? true : false;

  const handleDelete = (deleteTask: () => void) => {
    deleteTask();
    handleDeleteScreenClose();
  };

  return {
    deleteTaskId,
    handleDeleteScreenOpen,
    handleDeleteScreenClose,
    handleDelete,
    isDeleteModalOpen,
  };
};

export default useTaskDeleteViewModel;