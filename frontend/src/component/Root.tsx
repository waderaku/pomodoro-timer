import { Grid, Toolbar } from "@mui/material";
import { ROOT_TASK_ID } from "commonConstants";
import { selectedTaskIdState, userIdState } from "domain/hooks/taskViewModel";
import { useUserViewModel } from "domain/hooks/userViewModel";
import { useEffect } from "react";
import { useSetRecoilState } from "recoil";
import SideNavi from "./SideNavi";
import SignFeild from "./SignArea";
import TaskManager from "./TaskManager";
import ToolNavi from "./ToolNavi";

const Root = () => {
  // テスト用
  const { isSignIn } = useUserViewModel();
  const testUserId = "1";
  const setUserId = useSetRecoilState(userIdState);
  const defaultSelectedTaskId = ROOT_TASK_ID;
  const setSelectedTaskId = useSetRecoilState(selectedTaskIdState);
  useEffect(() => {
    setUserId(testUserId);
    setSelectedTaskId(defaultSelectedTaskId);
    // eslint-disable-next-line
  }, []);
  if (isSignIn) {
    return (
      <div>
        <ToolNavi />
        <Toolbar />
        <Grid container>
          <Grid item xs={2}>
            <SideNavi />
          </Grid>
          <Grid item xs={10}>
            <TaskManager />
          </Grid>
        </Grid>
      </div>
    );
  } else {
    return <SignFeild />;
  }
};

export default Root;
