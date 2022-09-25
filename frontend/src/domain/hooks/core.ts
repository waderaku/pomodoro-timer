import {
  fetchTaskAPI
} from "backendApi";
import {
  atom,
  selector,
  selectorFamily, useRecoilRefresher_UNSTABLE, useRecoilState,
  useRecoilValue,
  useRecoilValueLoadable
} from "recoil";
import {
  AuthToken,
  ChildrenTaskCount, Task, TaskId, TaskResponse, UserId
} from "../model";


const taskResponseState = selector<TaskResponse>({
  key: "taskResponse",
  get: async ({ get }) => {
    const token = get(authTokenState);
    if (!token) {
      throw Error("User is not yet logged in");
    }
    const taskResponse = await fetchTaskAPI(token);
    return taskResponse;
  },
});

export const taskPoolState = selector<Map<TaskId, Task>>({
  key: "taskPool",
  get: ({ get }) => {
    return get(taskResponseState).taskPool;
  },
});

// ショートカットタスクのうち未完了のものの配列をリターン
const shortcutTaskArrayState = selector<TaskId[]>({
  key: "shortcutTaskArray",
  get: ({ get }) =>
    get(taskResponseState).shortcutTaskArray.filter(
      (taskId) => !get(taskState(taskId)).done
    ),
});

export const taskState = selectorFamily<Task, TaskId>({
  key: "task",
  get:
    (taskId) =>
    ({ get }) => {
      const taskPool = get(taskPoolState);
      const task = taskPool.get(taskId);
      if (task) {
        return task;
      } else {
        throw new Error("Unexpected TaskId");
      }
    },
});

const childrenTaskCountState = selectorFamily<ChildrenTaskCount, TaskId>({
  key: "childrenTaskCount",
  get:
    (taskId) =>
    ({ get }) => {
      const task = get(taskState(taskId));
      const finishedTaskCount = task.childrenIdList.filter(
        (taskId) => get(taskState(taskId)).done
      ).length;
      const unfinishedTaskCount = task.childrenIdList.filter(
        (taskId) => !get(taskState(taskId)).done
      ).length;
      return {
        finishedTaskCount,
        unfinishedTaskCount,
      };
    },
});

export const useFinishedChildrenTaskCount = (taskId: TaskId) => {
  return useRecoilValue(childrenTaskCountState(taskId));
};

// 現在のTaskManagerに表示されるべきTaskのId
export const selectedTaskIdState = atom<TaskId>({
  key: "selectedTaskId",
});

// 現在選択されているTaskManagerに表示するべきTaskのIdを返す
export const useSelectedTaskId = (): TaskId => {
  return useRecoilValue(selectedTaskIdState);
};

export const userIdState = atom<UserId>({
  key: "userId",
});

export const useIsTaskLoaded = () => {
  return useRecoilValueLoadable(taskPoolState).state === "hasValue";
};

export const useHasChildTask = (taskId: TaskId) => {
  return useRecoilValue(taskState(taskId)).childrenIdList.length > 0;
};

export const useShortcutTaskArray = () => {
  return useRecoilValue(shortcutTaskArrayState);
};

export const useTaskValue = (taskId: TaskId): Task => {
  return useRecoilValue(taskState(taskId));
}

export const authTokenState = atom<AuthToken>({
  key: "authToken",
  default: "",
});

export const useAuthToken = () => {
  return useRecoilState(authTokenState)
}
export const useAuthTokenValue = () => {
  return useRecoilValue(authTokenState);
}

export const useRefresh = () => {
  return useRecoilRefresher_UNSTABLE(taskPoolState);
}