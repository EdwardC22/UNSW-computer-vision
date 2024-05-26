import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import {
  Label,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { Timeframe } from "../utils/data";
import { apiCall } from "../utils/helpers";
import { Center, ColorMode, Spinner, useColorMode } from "@chakra-ui/react";

interface Props {
  timeFrame: Timeframe;
  dateProp: string;
  label: string;
}

function makeXLabel(label: string, timeFrame: Timeframe) {
  if (timeFrame === Timeframe.daily) {
    return "Days";
  } else if (timeFrame === Timeframe.hourly) {
    return "Hours (24hr time)";
  } else if (timeFrame === Timeframe.monthly) {
    return "Months";
  }
}

function makeXAxis(num: number, timeFrame: Timeframe, datePassed: string) {
  switch (timeFrame) {
    case Timeframe.daily:
      const newDate = new Date(datePassed);
      newDate.setDate((newDate.getDay() + num - 2) % 7);
      return newDate.toLocaleDateString("en-US", { weekday: "long" });

    case Timeframe.hourly:
      return num;
    case Timeframe.monthly:
      const date = new Date();
      date.setMonth(num - 1);
      return date.toLocaleString("en-US", { month: "long" });
    default:
      return -1;
  }
}

function makeApiLabel(input: string) {
  // Apicalls require a different name
  if (input === "income") {
    return "income";
  } else if (input === "customerfrequency") {
    return "customer_frequency";
  } else {
    return "INVALID";
  }
}

function getTextColour(colorMode: ColorMode) {
  return colorMode === "dark" ? "white" : "black";
}

const TimeGraph = ({ timeFrame, dateProp, label }: Props) => {
  const { colorMode } = useColorMode();
  let { restaurantName } = useParams();
  let [data, setData] = useState<Array<any>>([]);
  const [loading, setLoading] = useState<boolean>(true);
  useEffect(() => {
    async function fetchData() {
      const apiDate: string | number =
        timeFrame === Timeframe.monthly ? dateProp.split("-")[0] : dateProp;
      try {
        const response: any = await apiCall(
          `/${restaurantName}/analysis/${timeFrame}${label}/${apiDate}`,
          {},
          "GET"
        );
        const array: Array<number> =
          response[`${timeFrame}_${makeApiLabel(label)}`];
        const newData = array.map((val, idx) => {
          const newObj: any = {};
          newObj[makeApiLabel(label)] = val;
          newObj["label"] = makeXAxis(idx + 1, timeFrame, dateProp);
          return newObj;
        });
        setData(newData);
        setLoading(false);
      } catch (err) {
        console.log(err);
      }
    }
    fetchData();
  }, [timeFrame, restaurantName, dateProp, label]);
  if (loading) {
    return (
      <Center>
        <Spinner color="purple" thickness="4px" size={"xl"} />
      </Center>
    );
  }
  return (
    <LineChart width={375} height={300} data={data}>
      <Line type="monotone" stroke="#8884d8" dataKey={makeApiLabel(label)} />
      <XAxis
        dataKey={"label"}
        style={{ fill: getTextColour(colorMode) }}
        height={40}
      >
        <Label
          value={makeXLabel(label, timeFrame)}
          offset={0}
          position="insideBottom"
          style={{ fill: getTextColour(colorMode) }}
        />
      </XAxis>
      <YAxis style={{ fill: getTextColour(colorMode) }} />
      <Tooltip labelStyle={{ color: "black" }} />
    </LineChart>
  );
};

export default TimeGraph;
