import { Box, Grid, GridItem, Img, Text } from "@chakra-ui/react";
import { SelectedMaterialsInterface } from "@/interfaces/Materials";
import { MEDIA_LOCAL, MEDIA_URL } from "@/local";

interface Props {
    material_parts: any[];
    selectedMaterial: SelectedMaterialsInterface;
    setSelectedMaterial: (selectedMaterial: SelectedMaterialsInterface) => void;
}

export const MaterialsSet = ({ material_parts, selectedMaterial, setSelectedMaterial }: Props) => {
    const handleSetMaterial = (partId: number, materialId: number) => {
        setSelectedMaterial({ ...selectedMaterial, [partId]: materialId });
    };

    return (
        <Box>
            {material_parts.map((part, key) => {
                // Проверяем, есть ли группы материалов с более чем одним материалом
                const hasMultipleMaterials = part.material_groups.length >= 1 &&
                    part.material_groups.some((group: any) => group.materials.length > 1);

                // Рендерим часть только если есть выбор материалов
                return hasMultipleMaterials ? (
                    <Box key={key}>
                        <Text>{part.name}</Text>
                        <Grid
                            mt='3'
                            mb='3'
                            w='100%'
                            gridTemplateColumns='repeat(auto-fill, 34px)'
                            gridTemplateRows='repeat(auto-fill, 34px)'
                            gap={1}
                        >
                            {part.material_groups.map((group: any, i: number) => (
                                group.materials.map((material: any, j: number) => (
                                    <GridItem
                                        key={`${i}-${j}`}
                                        p='2px'
                                        borderWidth='2px'
                                        borderColor={selectedMaterial[part.id] === material.id ? 'brown.500' : 'transparent'}
                                        onClick={() => handleSetMaterial(part.id, material.id)}
                                        cursor="pointer"
                                        _hover={{
                                            borderColor: 'orange.500'
                                        }}
                                    >
                                        {material?.color && (
                                            <Box w='26px' h='26px' bg={material.color.hex} />
                                        )}
                                        {material?.material && (
                                            <Img
                                                w='26px'
                                                h='26px'
                                                src={MEDIA_LOCAL ? MEDIA_URL + material.material.image : material.material.image}
                                                alt={`Material ${material.id}`}
                                            />
                                        )}
                                    </GridItem>
                                ))
                            ))}
                        </Grid>
                    </Box>
                ) : null;
            })}
        </Box>
    );
};