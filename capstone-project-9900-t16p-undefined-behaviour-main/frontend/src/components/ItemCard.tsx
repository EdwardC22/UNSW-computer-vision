import { Box, GridItem, Text, Image } from "@chakra-ui/react";

/// Component wraps a griditem to style what an menu item looks like

interface Props {
  item: DItem;
  catID: number;
  action: any;
}

const ItemCard = ({ item, catID, action }: Props) => {
  return (
    <GridItem>
      <Box
        borderTop="1px"
        borderColor={"rgba(0,0,0, 0.05)"}
        p={3}
        shadow="lg"
        borderRadius="lg"
        backgroundColor={"rgba(255,255,255,0.05)"}
      >
        {item.image ? (
          <Image
            src={item.image}
            boxSize="220px"
            alt={`Image describing restuarant item named ${item.name}`}
          />
        ) : (
          <></>
        )}
        <Text fontSize="xl">{item.name}</Text>
        <Text>{item.description}</Text>
        <Text>{item.ingredients}</Text>
        <Text>${item.cost}</Text>
        <Box display="flex" justifyContent={"flex-end"}>
          {action}
        </Box>
      </Box>
    </GridItem>
  );
};

export default ItemCard;
