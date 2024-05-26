import { Box, Flex, Heading, Image, Tag, Text } from "@chakra-ui/react";
import { useNavigate } from "react-router-dom";

/// This component is used to display an item to a customer while they are ordering
/// from the menu. On click the comonponent navigates the user to a separate page
/// displaying more information about the item/

interface Props {
  item: DItem;
}

const MenuItemDisplay = ({ item }: Props) => {
  const navigate = useNavigate();
  return (
    <>
      <Flex
        onClick={() => navigate(`${item.id}`, { state: { item } })}
        cursor={"pointer"}
        gap="10px"
        borderBlock="1px solid"
        paddingInline={"10px"}
        borderColor="rgba(211,211,211, .75)"
      >
        <Box
          flex="4"
          display="flex"
          flexDir={"column"}
          justifyContent={"center"}
        >
          <Flex justifyContent={"space-between"}>
            <Heading size={"md"}>{item.name}</Heading>
          </Flex>
          <Text overflowWrap={"anywhere"}>{item.description}</Text>
          <Flex>
            <Text>${item.cost}</Text>
            {item.popular && (
              <Tag size="md" marginLeft={15} colorScheme="green">
                Popular
              </Tag>
            )}
          </Flex>
        </Box>
        {item.image ? (
          <Box flex="1" paddingBlock="10px">
            <Image
              src={item.image}
              boxSize="100px"
              borderRadius={"sm"}
              alt={`Image describing restuarant item named ${item.name}`}
            />
          </Box>
        ) : (
          <></>
        )}
      </Flex>
    </>
  );
};

export default MenuItemDisplay;
