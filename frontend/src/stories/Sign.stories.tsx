import { ComponentMeta, ComponentStory } from "@storybook/react";
import SignField from "component/SignField";
import { RecoilRoot } from "recoil";

export default {
  title: "SignField/sample",
  component: SignField,
} as ComponentMeta<typeof SignField>;

const Template: ComponentStory<typeof SignField> = () => {
  return (
    <RecoilRoot>
      <SignField />
    </RecoilRoot>
  );
};

export const sample = Template.bind({});
