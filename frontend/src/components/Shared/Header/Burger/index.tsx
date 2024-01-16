import {Box, Flex} from "@chakra-ui/react";
import {motion} from "framer-motion";

const MotionBox = motion(Box);

interface BurgerProps {
  isOpen: boolean;
  setOpen: (isOpen: boolean) => void;
}

export const Burger = ({isOpen, setOpen}: BurgerProps) => {
  const w = '32px';
  const topBarAnimation = isOpen ? {rotate: 45, translateY: '10px'} : {rotate: 0, translateY: '0px'};
  const middleBarAnimation = isOpen ? {opacity: 0, marginLeft: '-80px'} : {opacity: 1, marginLeft: '0px'};
  const bottomBarAnimation = isOpen ? {rotate: -45, translateY: '-10px'} : {rotate: 0, translateY: '0px'};

  return (
    <Flex as="button" mr={3} w={w} h="24px"  direction={'column'} justify={'space-between'} alignItems={'center'}
          onClick={() => setOpen(!isOpen)}
          aria-label="Navigation Menu"
    >
      <MotionBox w={w} h={'4px'} bg={'brown.500'} initial={false} animate={topBarAnimation} transition={{duration: 0.5}}/>
      <MotionBox w={w} h={'4px'} bg={'brown.500'} initial={false} animate={middleBarAnimation} transition={{duration: 0.5}}/>
      <MotionBox w={w} h={'4px'} bg={'brown.500'} initial={false} animate={bottomBarAnimation} transition={{duration: 0.5}}/>
    </Flex>
  );
};
