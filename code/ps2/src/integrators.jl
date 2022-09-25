export VelocityVerlet
export take_one_step!, take_n_step!

abstract type Integrator end
struct VelocityVerlet <: Integrator end

struct StepTracker
    data::Matrix{Particle}
end

function take_one_step!(particles, i, Δt, ::VelocityVerlet)
    particle = particles[i]
    particle.v += accelerationof(particles, i) * Δt / 2  # 𝐯(t + Δt / 2)
    particle.r += particle.v * Δt  # 𝐫(t + Δt)
    𝐚 = accelerationof(particles, i)  # 𝐚(t + Δt)
    particle.v += 𝐚 * Δt / 2  # 𝐯(t + Δt)
    return particles
end
function take_one_step!(particles, Δt, ::VelocityVerlet)
    for i in eachindex(particles)
        take_one_step!(particles, i, Δt, VelocityVerlet())
    end
    return particles
end

function take_n_steps!(particles, n, Δt, ::VelocityVerlet)
    data = Matrix{Particle}(undef, length(particles), n)
    for i in 1:n
        data[:, i] = take_one_step!(particles, Δt, VelocityVerlet())
    end
    return StepTracker(data)
end
