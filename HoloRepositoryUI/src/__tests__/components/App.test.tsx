import React from "react";
import Enzyme, { shallow } from "enzyme";
import Adapter from "enzyme-adapter-react-16";
import App from "../../components/core/App";

Enzyme.configure({ adapter: new Adapter() });

it("renders without crashing", () => {
  shallow(<App />);
});
