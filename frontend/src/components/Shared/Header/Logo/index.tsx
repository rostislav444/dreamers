import {Box, Flex, Image, keyframes, usePrefersReducedMotion} from "@chakra-ui/react";


const pulsate = keyframes`
    0%, 100% {
        transform: scale(0.6);
    }
    50% {
        transform: scale(1.2);
    }
`;

export const Logo = ({mobile}: { mobile: boolean }) => {
    const prefersReducedMotion = usePrefersReducedMotion();

    const animation1 = prefersReducedMotion ? undefined : `${pulsate} 5s infinite`;
    const animation2 = prefersReducedMotion ? undefined : `${pulsate} 7s infinite`;
    const animation3 = prefersReducedMotion ? undefined : `${pulsate} 4s infinite`;

    const imageUrl = '/icons/sparkle.svg';

    return (
        <Flex justifyContent='center' alignItems='center'>
            <Box as='span' fontWeight={700} fontSize={mobile ? 28 : 36} mr={2}>Dreamers</Box>
            <Flex position='relative' w='12' h='12'>
                <Image animation={animation1} pos='absolute' top='4' left='1' w='9' h='9' src={imageUrl} alt='1'/>
                <Image animation={animation2} pos='absolute' top='-1' left='6' w='6' h='6' src={imageUrl} alt='2'/>
                <Image animation={animation3} pos='absolute' top='2' w='4' h='4' src={imageUrl} alt='3'/>
            </Flex>
        </Flex>
    );
};
