import {
  Heading,
  Table,
  TableCaption,
  TableContainer,
  Tbody,
  Td,
  Th,
  Thead,
  Tr,
} from "@chakra-ui/react";
import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { apiCall } from "../utils/helpers";
interface Props {
  timeFrame: string;
  dateProp: string;
}

interface ResponseType {
  mean: number;
  median: number;
  min: number;
  max: number;
}

const SummaryStatisticsTable = ({ timeFrame, dateProp }: Props) => {
  let { restaurantName } = useParams();
  const [data, setData] = useState<ResponseType>();
  useEffect(() => {
    async function fetchData() {
      const apiDate: string =
        timeFrame === "monthly"
          ? `${dateProp.split("-")[0]}-${dateProp.split("-")[1]}`
          : dateProp;
      try {
        const response: any = await apiCall(
          `/${restaurantName}/analysis/${timeFrame}orderstats/${apiDate}`,
          {},
          "GET"
        );
        const object: ResponseType = response;
        setData(object);
      } catch (err: any) {
        console.log("Error fetching order statistics", err.error);
      }
    }
    fetchData();
  }, [timeFrame, dateProp, restaurantName]);
  return (
    <>
      {data !== undefined && (
        <TableContainer>
          <Table>
            <TableCaption placement="top">$ Order Value</TableCaption>
            <Thead>
              <Tr>
                <Th style={{ paddingInline: "15px" }}>Mean</Th>
                <Th style={{ paddingInline: "15px" }}>Median</Th>
                <Th style={{ paddingInline: "15px" }}>Min</Th>
                <Th style={{ paddingInline: "15px" }}>Max</Th>
              </Tr>
            </Thead>
            <Tbody>
              <Tr>
                <Td style={{ paddingInline: "15px" }}>
                  ${data.mean.toFixed(2)}
                </Td>
                <Td style={{ paddingInline: "15px" }}>
                  ${data.median.toFixed(2)}
                </Td>
                <Td style={{ paddingInline: "15px" }}>
                  ${data.min.toFixed(2)}
                </Td>
                <Td style={{ paddingInline: "15px" }}>
                  ${data.max.toFixed(2)}
                </Td>
              </Tr>
            </Tbody>
          </Table>
        </TableContainer>
      )}
    </>
  );
};

export default SummaryStatisticsTable;
