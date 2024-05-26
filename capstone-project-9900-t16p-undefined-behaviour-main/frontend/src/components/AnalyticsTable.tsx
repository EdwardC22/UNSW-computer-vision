import {
  Box,
  Center,
  Flex,
  Select,
  Spinner,
  Table,
  TableContainer,
  Tbody,
  Td,
  Text,
  Th,
  Thead,
  Tr,
} from "@chakra-ui/react";
import { useEffect, useState } from "react";

type TableDataFormat = [string, number];
type Options = [string, string];

interface Props {
  label: string;
  data: TableDataFormat[];
  heading: string;
  options: Options;
  type: string;
  defaultOrder: Ordering;
}

enum Ordering {
  Normal = "Normal",
  Inverse = "Inverse",
}

const AnalyticsTable = ({
  label,
  data,
  heading,
  options,
  type,
  defaultOrder,
}: Props) => {
  const [loading, setLoading] = useState<boolean>(true);
  const [order, setOrder] = useState<Ordering>(defaultOrder);
  const [sortedData, setSortedData] = useState<TableDataFormat[]>(data);
  useEffect(() => {
    const newSort: TableDataFormat[] = [...data].sort(
      (a: TableDataFormat, b: TableDataFormat) =>
        order === Ordering.Inverse ? a[1] - b[1] : b[1] - a[1]
    );
    setSortedData(newSort);
    setLoading(false);
  }, [order, data]);

  if (loading) {
    return (
      <Center>
        <Spinner color="purple" thickness="4px" size={"xl"} />
      </Center>
    );
  }
  return (
    <Box maxWidth={400}>
      <Flex alignItems={"center"} gap={"5px"}>
        <Select
          value={order}
          onChange={(ev) => setOrder(ev.target.value as Ordering)}
          flex={1}
        >
          <option value={Ordering.Normal}>{options[0]}</option>
          <option value={Ordering.Inverse}>{options[1]}</option>
        </Select>
        <Text flex={2.5} fontSize="x-large">
          {heading}
        </Text>
      </Flex>
      <TableContainer maxWidth={400} maxHeight={300} overflowY={"scroll"}>
        <Table>
          <Thead>
            <Tr>
              <Th>Item Name</Th>
              <Th>{label}</Th>
            </Tr>
          </Thead>
          <Tbody>
            {loading && (
              <Tr>
                <Td>
                  <Spinner color="purple" thickness="4px" size={"xl"} />
                </Td>
              </Tr>
            )}
            {!loading &&
              sortedData.map((item: [string, number], idx: number) => (
                <Tr key={`${label}${idx}`}>
                  <Td>{item[0]}</Td>
                  <Td>
                    {type === "speed"
                      ? `${item[1].toString().slice(0, 2)}:${item[1]
                          .toString()
                          .slice(2, 4)}`
                      : item[1]}
                  </Td>
                </Tr>
              ))}
          </Tbody>
        </Table>
      </TableContainer>
    </Box>
  );
};

export default AnalyticsTable;
