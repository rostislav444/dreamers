import {Box, Flex} from "@chakra-ui/react";
import {ReactNode} from "react";

interface ImagePaginationProps {
  onHover: any
}

export const ImagePagination = ({onHover}: ImagePaginationProps) => (
  <Box
    onMouseEnter={onHover}
    position="relative"
    display="block"
    height="100%"
    width="100%"
    cursor='pointer'
    backgroundColor="transparent"
    borderBottom="3px solid transparent"
    _hover={{
      borderBottomColor: "brown.500 !important",
    }}
  />
);

interface ImagePaginationWrapperProps {
  children: ReactNode;
}

export const ImagePaginationWrapper = ({children}: ImagePaginationWrapperProps) => (
  <Flex
    position="absolute"
    cursor='pointer'
    top="0"
    width="100%"
    height="100%"
    display="flex"
    zIndex="100"
    _hover={{
      "> div": {
        borderBottomColor: "brown.100",
      },
    }}
  >
    {children}
  </Flex>
);