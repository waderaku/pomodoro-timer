import { deleteTaskAPI, registerTaskAPI, updateTaskAPI } from "backendApi";
import { selectedTaskIdState, useAuthTokenValue, useRefresh, useTaskValue } from "domain/hooks/core";
import { Deadline, Minute, Notes, ShortcutFlg, TaskId, TaskName, TaskViewModel } from "domain/model";
import { useSetRecoilState } from "recoil";


// TaskViewModelをリターンする
const useTaskViewModel = (taskId: TaskId): TaskViewModel => {
  // Task取得
  const task = useTaskValue(taskId);

  // AuthToken取得
  const token = useAuthTokenValue();

  // API呼び出し後の画面更新関数
  const refresh = useRefresh();

  // TaskCreatorとサイドバーのプロジェクトの追加で使われるタスク追加
  const createTask = async (
    taskName: TaskName,
    estimatedWorkload: Minute,
    deadline: Deadline,
    notes: Notes,
    shortcutFlg: ShortcutFlg
  ) => {
    await registerTaskAPI(
      token,
      task.id,
      taskName,
      estimatedWorkload,
      deadline,
      notes,
      shortcutFlg
    );
    refresh();
  };

  // TaskSummaryCardでfinishタスクが押下されたとき
  const finishTask = async () => {
    if (task.done) {
      throw new Error("This task is already done");
    }
    const newTask = { ...task, done: true };
    await updateTaskAPI(token, newTask);
    refresh();
  };

  // Configモーダルでtaskの編集がなされた時
  const updateTask = (
    taskName: TaskName,
    estimatedWorkload: Minute,
    deadline: Deadline,
    notes: Notes,
    shortcutFlg: ShortcutFlg
  ) => {
    const newTask = {
      ...task,
      name: taskName,
      estimatedWorkload,
      deadline,
      notes,
      shortcutFlg,
    };
    updateTaskAPI(token, newTask);
    refresh();
  };

  // タスクの削除
  const deleteTask = async () => {
    await deleteTaskAPI(token, taskId);
    refresh();
  };

  const setSelectedTaskId = useSetRecoilState(selectedTaskIdState);

  // タスクマネージャー画面へ遷移
  const toManager = () => setSelectedTaskId(task.id);

  return {
    task,
    createTask,
    finishTask,
    updateTask,
    toManager,
    deleteTask,
  };
};

export default useTaskViewModel;