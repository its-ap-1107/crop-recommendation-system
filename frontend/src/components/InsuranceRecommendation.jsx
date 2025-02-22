import PropTypes from 'prop-types';
import {
  Box,
  Card,
  CardContent,
  Typography,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Chip,
  Button,
  LinearProgress,
  Grid,
  Alert,
  Divider,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow
} from '@mui/material';
import {
  CheckCircle,
  Warning,
  Error,
  ArrowUpward,
  ArrowDownward,
  LocalHospital,
  FamilyRestroom,
  MonetizationOn,
  Speed,
  ExpandMore,
  LocalHotel,
  AccessTime,
  Block,
  LocalShipping
} from '@mui/icons-material';

const RiskLevelIcon = ({ level }) => {
  switch (level.toLowerCase()) {
    case 'low':
      return <CheckCircle color="success" />;
    case 'moderate':
      return <Warning color="warning" />;
    case 'high':
      return <Error color="error" />;
    default:
      return <Speed color="primary" />;
  }
};

RiskLevelIcon.propTypes = {
  level: PropTypes.string.isRequired
};

const PlanDetails = ({ plan }) => (
  <Box sx={{ mt: 2 }}>
    {/* Premium Range */}
    <TableContainer component={Paper} variant="outlined" sx={{ mb: 2 }}>
      <Table size="small">
        <TableHead>
          <TableRow>
            <TableCell>Minimum Premium</TableCell>
            <TableCell>Maximum Premium</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          <TableRow>
            <TableCell>₹{plan.premium_range.min.toLocaleString()}</TableCell>
            <TableCell>₹{plan.premium_range.max.toLocaleString()}</TableCell>
          </TableRow>
        </TableBody>
      </Table>
    </TableContainer>

    {/* Coverage Details */}
    <Accordion>
      <AccordionSummary expandIcon={<ExpandMore />}>
        <Typography variant="subtitle2" sx={{ display: 'flex', alignItems: 'center' }}>
          <LocalHotel sx={{ mr: 1 }} /> Coverage Details
        </Typography>
      </AccordionSummary>
      <AccordionDetails>
        <List dense>
          {plan.coverage_details.map((detail, idx) => (
            <ListItem key={idx}>
              <ListItemIcon>
                <CheckCircle color="success" fontSize="small" />
              </ListItemIcon>
              <ListItemText primary={detail} />
            </ListItem>
          ))}
        </List>
      </AccordionDetails>
    </Accordion>

    {/* Key Benefits */}
    <Accordion>
      <AccordionSummary expandIcon={<ExpandMore />}>
        <Typography variant="subtitle2" sx={{ display: 'flex', alignItems: 'center' }}>
          <CheckCircle sx={{ mr: 1 }} /> Key Benefits
        </Typography>
      </AccordionSummary>
      <AccordionDetails>
        <List dense>
          {plan.key_benefits.map((benefit, idx) => (
            <ListItem key={idx}>
              <ListItemIcon>
                <CheckCircle color="primary" fontSize="small" />
              </ListItemIcon>
              <ListItemText primary={benefit} />
            </ListItem>
          ))}
        </List>
      </AccordionDetails>
    </Accordion>

    {/* Waiting Periods */}
    <Accordion>
      <AccordionSummary expandIcon={<ExpandMore />}>
        <Typography variant="subtitle2" sx={{ display: 'flex', alignItems: 'center' }}>
          <AccessTime sx={{ mr: 1 }} /> Waiting Periods
        </Typography>
      </AccordionSummary>
      <AccordionDetails>
        <List dense>
          {plan.waiting_periods.map((period, idx) => (
            <ListItem key={idx}>
              <ListItemIcon>
                <AccessTime color="warning" fontSize="small" />
              </ListItemIcon>
              <ListItemText primary={period} />
            </ListItem>
          ))}
        </List>
      </AccordionDetails>
    </Accordion>

    {/* Exclusions */}
    <Accordion>
      <AccordionSummary expandIcon={<ExpandMore />}>
        <Typography variant="subtitle2" sx={{ display: 'flex', alignItems: 'center' }}>
          <Block sx={{ mr: 1 }} /> Exclusions
        </Typography>
      </AccordionSummary>
      <AccordionDetails>
        <List dense>
          {plan.exclusions.map((exclusion, idx) => (
            <ListItem key={idx}>
              <ListItemIcon>
                <Block color="error" fontSize="small" />
              </ListItemIcon>
              <ListItemText primary={exclusion} />
            </ListItem>
          ))}
        </List>
      </AccordionDetails>
    </Accordion>

    {/* Network Hospitals & Claims */}
    {(plan.network_hospitals || plan.claim_process) && (
      <Accordion>
        <AccordionSummary expandIcon={<ExpandMore />}>
          <Typography variant="subtitle2" sx={{ display: 'flex', alignItems: 'center' }}>
            <LocalShipping sx={{ mr: 1 }} /> Network & Claims
          </Typography>
        </AccordionSummary>
        <AccordionDetails>
          {plan.network_hospitals && (
            <Typography variant="body2" gutterBottom>
              <strong>Network Hospitals:</strong> {plan.network_hospitals}
            </Typography>
          )}
          {plan.claim_process && (
            <Typography variant="body2">
              <strong>Claim Process:</strong> {plan.claim_process}
            </Typography>
          )}
        </AccordionDetails>
      </Accordion>
    )}
  </Box>
);

PlanDetails.propTypes = {
  plan: PropTypes.shape({
    premium_range: PropTypes.shape({
      min: PropTypes.number.isRequired,
      max: PropTypes.number.isRequired
    }).isRequired,
    coverage_details: PropTypes.arrayOf(PropTypes.string).isRequired,
    key_benefits: PropTypes.arrayOf(PropTypes.string).isRequired,
    waiting_periods: PropTypes.arrayOf(PropTypes.string).isRequired,
    exclusions: PropTypes.arrayOf(PropTypes.string).isRequired,
    network_hospitals: PropTypes.string,
    claim_process: PropTypes.string
  }).isRequired
};

const InsuranceRecommendation = ({ assessmentData }) => {
  if (!assessmentData) return null;

  const { risk_assessment, recommendations } = assessmentData;

  const getRiskColor = (level) => {
    switch (level.toLowerCase()) {
      case 'low':
        return 'success.main';
      case 'moderate':
        return 'warning.main';
      case 'high':
        return 'error.main';
      default:
        return 'primary.main';
    }
  };

  return (
    <Box sx={{ maxWidth: 1200, margin: '0 auto', p: 3 }}>
      {/* Risk Assessment Section */}
      <Card sx={{ mb: 4 }}>
        <CardContent>
          <Typography variant="h5" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <RiskLevelIcon level={risk_assessment.risk_level} />
            Risk Assessment
          </Typography>
          
          <Grid container spacing={3} sx={{ mb: 3 }}>
            <Grid item xs={12} md={4}>
              <Typography variant="subtitle1" gutterBottom>Risk Level</Typography>
              <Chip
                label={risk_assessment.risk_level.toUpperCase()}
                color={risk_assessment.risk_level.toLowerCase()}
                sx={{
                  bgcolor: getRiskColor(risk_assessment.risk_level),
                  color: 'white'
                }}
              />
            </Grid>
            
            <Grid item xs={12} md={4}>
              <Typography variant="subtitle1" gutterBottom>Risk Score</Typography>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <LinearProgress
                  variant="determinate"
                  value={risk_assessment.risk_score * 100}
                  sx={{ flexGrow: 1 }}
                />
                <Typography variant="body2">
                  {Math.round(risk_assessment.risk_score * 100)}%
                </Typography>
              </Box>
            </Grid>
            
            <Grid item xs={12} md={4}>
              <Typography variant="subtitle1" gutterBottom>Confidence</Typography>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <LinearProgress
                  variant="determinate"
                  value={risk_assessment.risk_confidence}
                  sx={{ flexGrow: 1 }}
                />
                <Typography variant="body2">
                  {Math.round(risk_assessment.risk_confidence)}%
                </Typography>
              </Box>
            </Grid>
          </Grid>

          <Divider sx={{ my: 2 }} />
          
          {/* Risk Factors */}
          <Grid container spacing={3}>
            <Grid item xs={12} md={6}>
              <Typography variant="h6" color="error" gutterBottom>
                Risk Factors
              </Typography>
              <List dense>
                {risk_assessment.risk_factors.map((factor, index) => (
                  <ListItem key={index}>
                    <ListItemIcon>
                      <ArrowUpward color="error" />
                    </ListItemIcon>
                    <ListItemText primary={factor} />
                  </ListItem>
                ))}
              </List>
            </Grid>
            
            <Grid item xs={12} md={6}>
              <Typography variant="h6" color="success.main" gutterBottom>
                Positive Factors
              </Typography>
              <List dense>
                {risk_assessment.positive_factors.map((factor, index) => (
                  <ListItem key={index}>
                    <ListItemIcon>
                      <ArrowDownward color="success" />
                    </ListItemIcon>
                    <ListItemText primary={factor} />
                  </ListItem>
                ))}
              </List>
            </Grid>
          </Grid>
        </CardContent>
      </Card>

      {/* Recommendations Section */}
      <Card>
        <CardContent>
          <Typography variant="h5" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <LocalHospital color="primary" />
            Insurance Recommendations
          </Typography>

          <Alert severity="info" sx={{ mb: 3 }}>
            Recommended Plan Type: {recommendations.recommended_plan_type}
          </Alert>

          <Grid container spacing={3}>
            {recommendations.matching_plans.map((plan, index) => (
              <Grid item xs={12} md={6} key={index}>
                <Card variant="outlined">
                  <CardContent>
                    <Typography variant="h6" gutterBottom>
                      {plan.plan_name}
                    </Typography>
                    <Typography variant="subtitle2" color="text.secondary" gutterBottom>
                      {plan.provider}
                    </Typography>
                    
                    <Box sx={{ my: 2 }}>
                      {plan.features.map((feature, idx) => (
                        <Chip
                          key={idx}
                          label={feature}
                          size="small"
                          sx={{ m: 0.5 }}
                        />
                      ))}
                    </Box>

                    {plan.premium_info.starting_from && (
                      <Typography variant="body2" color="primary" gutterBottom>
                        <MonetizationOn sx={{ fontSize: 16, mr: 1, verticalAlign: 'text-bottom' }} />
                        Starting from: {plan.premium_info.starting_from}
                      </Typography>
                    )}

                    {plan.premium_info.coverage_amount && (
                      <Typography variant="body2" color="success.main" gutterBottom>
                        <FamilyRestroom sx={{ fontSize: 16, mr: 1, verticalAlign: 'text-bottom' }} />
                        {plan.premium_info.coverage_amount}
                      </Typography>
                    )}

                    <PlanDetails plan={plan} />

                    <Button
                      variant="contained"
                      color="primary"
                      fullWidth
                      href={plan.url}
                      target="_blank"
                      sx={{ mt: 2 }}
                    >
                      View Plan Details
                    </Button>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>

          <Box sx={{ mt: 3 }}>
            <Typography variant="h6" gutterBottom>Recommendation Justification</Typography>
            <List dense>
              {recommendations.justification.map((reason, index) => (
                <ListItem key={index}>
                  <ListItemIcon>
                    <CheckCircle color="primary" />
                  </ListItemIcon>
                  <ListItemText primary={reason} />
                </ListItem>
              ))}
            </List>
          </Box>
        </CardContent>
      </Card>
    </Box>
  );
};

InsuranceRecommendation.propTypes = {
  assessmentData: PropTypes.shape({
    risk_assessment: PropTypes.shape({
      risk_level: PropTypes.string.isRequired,
      risk_score: PropTypes.number.isRequired,
      risk_confidence: PropTypes.number.isRequired,
      risk_factors: PropTypes.arrayOf(PropTypes.string).isRequired,
      positive_factors: PropTypes.arrayOf(PropTypes.string).isRequired,
      risk_probabilities: PropTypes.shape({
        low: PropTypes.number.isRequired,
        moderate: PropTypes.number.isRequired,
        high: PropTypes.number.isRequired
      }).isRequired
    }).isRequired,
    recommendations: PropTypes.shape({
      recommended_plan_type: PropTypes.string.isRequired,
      matching_plans: PropTypes.arrayOf(PropTypes.shape({
        provider: PropTypes.string.isRequired,
        plan_name: PropTypes.string.isRequired,
        description: PropTypes.string,
        url: PropTypes.string.isRequired,
        features: PropTypes.arrayOf(PropTypes.string).isRequired,
        premium_info: PropTypes.shape({
          starting_from: PropTypes.string,
          coverage_amount: PropTypes.string
        }).isRequired,
        premium_range: PropTypes.shape({
          min: PropTypes.number.isRequired,
          max: PropTypes.number.isRequired
        }).isRequired,
        coverage_details: PropTypes.arrayOf(PropTypes.string).isRequired,
        key_benefits: PropTypes.arrayOf(PropTypes.string).isRequired,
        waiting_periods: PropTypes.arrayOf(PropTypes.string).isRequired,
        exclusions: PropTypes.arrayOf(PropTypes.string).isRequired,
        network_hospitals: PropTypes.string,
        claim_process: PropTypes.string
      })).isRequired,
      justification: PropTypes.arrayOf(PropTypes.string).isRequired
    }).isRequired
  })
};

export default InsuranceRecommendation; 