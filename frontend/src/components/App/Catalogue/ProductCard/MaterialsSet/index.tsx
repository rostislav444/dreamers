import {Box, Grid, GridItem, Img, Text} from "@chakra-ui/react";
import {SelectedMaterialsInterface} from "@/interfaces/Materials";
import {MEDIA_LOCAL, MEDIA_URL} from "@/local";


interface Props {
    material_parts: any[]
    selectedMaterial: SelectedMaterialsInterface
    setSelectedMaterial: (selectedMaterial: SelectedMaterialsInterface) => void
}


export const MaterialsSet = ({material_parts, selectedMaterial, setSelectedMaterial}: Props) => {
    const handleSetMaterial = (partId: number, materialId: number) => {
        setSelectedMaterial({...selectedMaterial, [partId]: materialId})
    }

    return <Box>
        {
            material_parts.map((part, key) => {
                return <Box key={key}>
                    <Text>{part.name}</Text>
                    <Grid mt='3' mb='3' w='100%'
                          gridTemplateColumns='repeat(auto-fill, 34px)'
                          gridTemplateRows='repeat(auto-fill, 34px)'
                          gap={1}
                    >
                        {part.material_groups.map((group: any, i: number) => {
                            return group.materials.map((material: any, j: number) => {
                                return <GridItem
                                    key={j}
                                    p='2px'
                                    borderWidth='2px'
                                    borderColor={selectedMaterial[part.id] === material.id ? 'brown.500' : 'transparent'}
                                    onClick={() => handleSetMaterial(part.id, material.id)}
                                >
                                    {material?.color && (<Box w='26px' h='26px' bg={material.color.hex}/>)}
                                    {material?.material && (<Img w='26px' h='26px' src={MEDIA_LOCAL ? MEDIA_URL + material.material.image : material.material.image}/>)}
                                </GridItem>
                            })
                        })}
                    </Grid>
                </Box>
            })
        }
    </Box>
}