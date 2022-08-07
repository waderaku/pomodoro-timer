import { useSetRecoilState } from "recoil";
import TaskManager from "./TaskManager";
import ToolNavi from "./ToolNavi";
import SideNavi from "./SideNavi";
import SignFeild from "./SignField";
import { selectedTaskIdState, userIdState } from "domain/hooks/taskViewModel";
import { useUserViewModel } from "domain/hooks/userViewModel";
import { useEffect, Suspense } from "react";
import { Grid, Toolbar, Typography } from "@mui/material";
import { ROOT_TASK_ID } from "commonConstants";

const Root = () => {
  // テスト用
  const { token } = useUserViewModel();
  const testUserId = "1";
  const setUserId = useSetRecoilState(userIdState);
  const defaultSelectedTaskId = ROOT_TASK_ID;
  const setSelectedTaskId = useSetRecoilState(selectedTaskIdState);
  useEffect(() => {
    setUserId(testUserId);
    setSelectedTaskId(defaultSelectedTaskId);
    // eslint-disable-next-line
  }, []);
  if (token) {
    return (
      <Suspense fallback={<Typography>Loading...</Typography>}>
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
      </Suspense>
    );
  } else {
    return <SignFeild />;
  }
};

export default Root;
