import {
  Box,
  Button,
  Container,
  Flex,
  Grid,
  GridItem,
  Heading,
  Input,
  Select,
  Text,
} from "@chakra-ui/react";
import { useNavigate, useParams } from "react-router-dom";
import ThemeToggle from "../components/ThemeToggle";
import { Link as RouterLink } from "react-router-dom";
import { apiCall, decodeRestaurantName } from "../utils/helpers";
import AnalyticsDataPicker from "../components/AnalyticsDatePicker";
import { useEffect, useState } from "react";
import { Timeframe } from "../utils/data";
import TimeGraph from "../components/TimeGraph";
import SummaryStatisticsTable from "../components/SummaryStatisticsTable";
import AnalyticsTable from "../components/AnalyticsTable";

type fastType = [string, string];
type TableDataFormat = [string, number];
enum Ordering {
  Normal = "Normal",
  Inverse = "Inverse",
}

/// Manager analytics page

const Analytics = () => {
  let { restaurantName } = useParams();
  const dateNow = new Date(Date.now()).toISOString().split("T")[0];
  const navigate = useNavigate();
  useEffect(() => {
    function verifyAccess() {
      apiCall(`/${restaurantName}/verifytoken`, {}, "POST").catch((err) => {
        console.log("User not authorised");
        navigate(`../`);
      });
    }
    verifyAccess();
  }, [restaurantName, navigate]);

  const [incomeDate, setIncomeDate] = useState<string>(dateNow);
  const [incomeTimeframe, setIncomeTimeframe] = useState<Timeframe>(
    Timeframe.hourly
  );
  const [freqDate, setFreqDate] = useState<string>(dateNow);
  const [freqTimeframe, setFreqTimeframe] = useState<Timeframe>(
    Timeframe.hourly
  );
  const [summDate, setSummDate] = useState<string>(dateNow);
  const [summTimeframe, setSummTimeframe] = useState<string>("weekly");

  const [popularItems, setPopularItems] = useState<TableDataFormat[]>([]);
  const [fastestItems, setFastestItems] = useState<TableDataFormat[]>([]);
  useEffect(() => {
    async function fetchPopularItems() {
      try {
        const response: any = await apiCall(
          `/${restaurantName}/analysis/itempopularity`,
          {},
          "GET"
        );
        setPopularItems(response.items);
      } catch (err) {
        console.log(err);
      }
    }
    fetchPopularItems();

    async function fetchFastestItems() {
      try {
        const response: any = await apiCall(
          `/${restaurantName}/analysis/itemspeed`,
          {},
          "GET"
        );
        const filtered = response.items.map((tup: fastType) => {
          const timeString = tup[1];
          const timeSplit = timeString.split(":");
          const hours = parseInt(timeSplit[0]);
          const minutes = parseInt(timeSplit[1]);
          const seconds = parseInt(timeSplit[2]);
          const totalMinutes = (hours * 60 + minutes) * 100 + seconds;
          return [tup[0], totalMinutes];
        });
        setFastestItems(filtered);
      } catch (err) {
        console.log(err);
      }
    }
    fetchFastestItems();
  }, []);
  return (
    <Container maxWidth="1275px" display="flex" flexDir="column" gap="15px">
      <Box display="flex" justifyContent={"space-between"}>
        <Heading textAlign={"center"}>
          {decodeRestaurantName(restaurantName)} Analytics
        </Heading>
        <ThemeToggle />
      </Box>
      <Flex justifyContent={"space-between"}>
        <Button colorScheme={"teal"} as={RouterLink} to="../dashboard">
          Dashboard
        </Button>
        <Button
            colorScheme={"gray"}
            onClick={() => {
              apiCall("/logout", {}, "POST");
              navigate(`/${restaurantName}/staff`);
            }}
          >
            Log out
          </Button>
      </Flex>
      <Grid
        templateColumns="repeat(auto-fit, minmax(400px, 1fr))"
        gridGap={"10px"}
      >
        <GridItem>
          <Box
            borderTop="1px"
            borderColor={"rgba(0,0,0, 0.05)"}
            p={3}
            shadow="lg"
            borderRadius="lg"
            backgroundColor={"rgba(255,255,255,0.05)"}
          >
            <AnalyticsTable
              options={["Most", "Least"]}
              heading={"Popular Items"}
              label={"Quantity"}
              data={popularItems}
              type={"pop"}
              defaultOrder={Ordering.Normal}
            />
          </Box>
        </GridItem>
        <GridItem>
          <Box
            borderTop="1px"
            borderColor={"rgba(0,0,0, 0.05)"}
            p={3}
            shadow="lg"
            borderRadius="lg"
            backgroundColor={"rgba(255,255,255,0.05)"}
          >
            <AnalyticsTable
              options={["Slowest", "Fastest"]}
              heading={"Delivered Items"}
              label={"Time (mins:seconds)"}
              data={fastestItems}
              type={"speed"}
              defaultOrder={Ordering.Inverse}
            />
          </Box>
        </GridItem>
        <GridItem>
          <Box
            borderTop="1px"
            borderColor={"rgba(0,0,0, 0.05)"}
            p={3}
            shadow="lg"
            borderRadius="lg"
            backgroundColor={"rgba(255,255,255,0.05)"}
          >
            <Flex>
              <Text fontSize="x-large" flex={2}>
                Order Statistics
              </Text>
              <Flex flexDir="column" gap="3px">
                <Select
                  placeholder="Select Timeframe:"
                  onChange={(ev) => {
                    if (ev.target.value === "") return;
                    setSummTimeframe(ev.target.value);
                  }}
                  value={summTimeframe}
                >
                  <option value={"daily"}>Daily</option>
                  <option value={"weekly"}>Weekly</option>
                  <option value={"monthly"}>Monthly</option>
                </Select>
                <Input
                  type="date"
                  value={summDate}
                  onChange={(ev) => {
                    setSummDate(ev.target.value);
                  }}
                />
              </Flex>
            </Flex>
            {summDate !== undefined && summTimeframe !== undefined && (
              <SummaryStatisticsTable
                timeFrame={summTimeframe}
                dateProp={summDate}
              />
            )}
          </Box>
        </GridItem>
        <GridItem>
          <Box
            borderTop="1px"
            borderColor={"rgba(0,0,0, 0.05)"}
            p={3}
            shadow="lg"
            borderRadius="lg"
            backgroundColor={"rgba(255,255,255,0.05)"}
          >
            <Flex flexDir={"row"}>
              <Text fontSize="x-large" flex={2}>
                Income Over Time
              </Text>
              <AnalyticsDataPicker
                selectVal={incomeTimeframe}
                date={incomeDate}
                selectHandler={setIncomeTimeframe}
                dateHandler={setIncomeDate}
              />
            </Flex>
            {incomeDate !== undefined && incomeTimeframe !== undefined && (
              <TimeGraph
                label="income"
                dateProp={incomeDate}
                timeFrame={incomeTimeframe}
              />
            )}
          </Box>
        </GridItem>
        <GridItem>
          <Box
            borderTop="1px"
            borderColor={"rgba(0,0,0, 0.05)"}
            p={3}
            shadow="lg"
            borderRadius="lg"
            backgroundColor={"rgba(255,255,255,0.05)"}
          >
            <Flex flexDir={"row"}>
              <Text fontSize="x-large" flex={2}>
                Customer Frequency
              </Text>
              <AnalyticsDataPicker
                selectVal={freqTimeframe}
                date={freqDate}
                selectHandler={setFreqTimeframe}
                dateHandler={setFreqDate}
              />
            </Flex>
            {freqDate !== undefined && freqTimeframe !== undefined && (
              <TimeGraph
                label="customerfrequency"
                dateProp={freqDate}
                timeFrame={freqTimeframe}
              />
            )}
          </Box>
        </GridItem>
      </Grid>
    </Container>
  );
};

export default Analytics;
