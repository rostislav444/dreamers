import {Box, Flex, Grid, Heading} from "@chakra-ui/react";
import {ChevronUpIcon} from "@chakra-ui/icons";
import Image from 'next/image';
import {MEDIA_URL} from "@/local";

interface ProductInteriorProps {
    mobile: boolean;
    currentCamera: any;
    selectedInterior: any[];
    showInterior: boolean;
    setShowInterior: (show: boolean) => void;
    handleSelectedInterior: (key: number, materialKey: number | null) => void;
}

export const ProductInterior = ({
                             mobile,
                             currentCamera,
                             selectedInterior,
                             showInterior,
                             setShowInterior,
                             handleSelectedInterior
                         }: ProductInteriorProps) => {
    const hasInterior = currentCamera.interior_layers.length > 0;

    if (!hasInterior) return null;

    return (
        <Box>
            <Flex
                justifyContent='space-between'
                alignItems='center'
                onClick={() => setShowInterior(!showInterior)}
            >
                <Heading size='md'>Інтер&apos;ер</Heading>
                <ChevronUpIcon
                    w='6'
                    h='6'
                    color='brown.500'
                    cursor='pointer'
                    transform={showInterior ? 'rotate(180deg)' : 'rotate(0deg)'}
                />
            </Flex>
            {showInterior && (
                <Box mt='4'>
                    {currentCamera.interior_layers.map((layer: any, key: number) => (
                        <Grid
                            gridTemplateColumns={mobile ?
                                'repeat(auto-fill, minmax(60px, 1fr))' :
                                'repeat(auto-fill, minmax(100px, 1fr))'
                            }
                            gap={2}
                            mb='2'
                            key={key}
                        >
                            <Box
                                borderWidth='2px'
                                borderColor={selectedInterior[key] === null ? 'brown.500' : 'white'}
                                onClick={() => handleSelectedInterior(key, null)}
                            />
                            {layer.materials.map((material: any, materialKey: number) => (
                                <Box
                                    pos='relative'
                                    borderWidth='2px'
                                    key={materialKey}
                                    pt='66%'
                                    borderColor={selectedInterior[key] === materialKey ? 'brown.500' : 'white'}
                                >
                                    <Image
                                        fill={true}
                                        onClick={() => handleSelectedInterior(key, materialKey)}
                                        quality={100}
                                        src={MEDIA_URL + material.image_thumbnails?.s}
                                        alt='img'
                                    />
                                </Box>
                            ))}
                        </Grid>
                    ))}
                </Box>
            )}
        </Box>
    );
};

export default ProductInterior;