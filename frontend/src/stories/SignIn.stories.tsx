import { ComponentMeta, ComponentStory } from "@storybook/react";
import SignInField from "component/SignArea/SignInArea";
import { RecoilRoot } from "recoil";

export default {
  title: "SignField/SignInField",
  component: SignInField,
} as ComponentMeta<typeof SignInField>;

const Template: ComponentStory<typeof SignInField> = () => {
  return (
    <RecoilRoot>
      <SignInField />
    </RecoilRoot>
  );
};

export const sample = Template.bind({});
