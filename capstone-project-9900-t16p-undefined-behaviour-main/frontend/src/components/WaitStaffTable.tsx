import {
  Box,
  Heading,
  Table,
  TableContainer,
  Tbody,
  Th,
  Thead,
  Tr,
} from "@chakra-ui/react";

/// Generic table used by waitstaff to display data

interface Props {
  headings: Array<string>;
  title: string;
  body: any;
}

const WaitStaffTable = ({ body, title, headings }: Props) => {
  return (
    <Box textAlign={"center"}>
      <Heading fontSize={"1.25rem"}>{title}</Heading>
      <TableContainer>
        <Table>
          <Thead>
            <Tr>
              {headings.map((title, idx) => (
                <Th key={idx}>{title}</Th>
              ))}
            </Tr>
          </Thead>
          <Tbody>{body}</Tbody>
        </Table>
      </TableContainer>
    </Box>
  );
};

export default WaitStaffTable;
