import {
  Accordion,
  AccordionButton,
  AccordionIcon,
  AccordionItem,
  AccordionPanel,
  Box,
  Heading,
} from "@chakra-ui/react";
import MenuItemDisplay from "./MenuItemDisplay";

/// Component displays categories and items inside of the categories
/// for a customer ordering from the menu

interface Props {
  categories: Array<DCategory>;
}

const Menu = ({ categories }: Props) => {
  return (
    <>
      <Accordion allowMultiple defaultIndex={[0]} padding="0">
        {categories.map((category, index) => (
          <AccordionItem key={`orderCategory${index}`} padding="0">
            <AccordionButton>
              <Box flex="1" textAlign="left">
                <Heading>{category.name}</Heading>
              </Box>
              <AccordionIcon />
            </AccordionButton>
            <AccordionPanel padding="0">
              {category.items.map((item, idx) => (
                <MenuItemDisplay item={item} key={idx} />
              ))}
            </AccordionPanel>
          </AccordionItem>
        ))}
      </Accordion>
    </>
  );
};

export default Menu;
