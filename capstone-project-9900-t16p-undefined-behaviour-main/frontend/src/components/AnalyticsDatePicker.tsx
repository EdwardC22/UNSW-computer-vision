import { Flex, Input, Select } from "@chakra-ui/react";
import { Timeframe } from "../utils/data";
interface Props {
  selectVal: Timeframe;
  date: string;
  selectHandler: any;
  dateHandler: any;
}

const AnalyticsDataPicker = ({
  selectVal,
  date,
  selectHandler,
  dateHandler,
}: Props) => {
  return (
    <Flex flexDir="column" gap="3px">
      <Select
        placeholder="Select Timeframe:"
        onChange={(ev) => {
          if (ev.target.value === "") return;
          selectHandler(ev.target.value);
        }}
        value={selectVal}
      >
        <option value={Timeframe.hourly}>Hourly</option>
        <option value={Timeframe.daily}>Daily</option>
        <option value={Timeframe.monthly}>Monthly</option>
      </Select>
      <Input
        type="date"
        value={date.toString()}
        onChange={(ev) => dateHandler(ev.target.value)}
      />
    </Flex>
  );
};

export default AnalyticsDataPicker;
